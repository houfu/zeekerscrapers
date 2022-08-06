import requests
import scrapy
from scrapy import FormRequest

from pdpcSpider.items import CommissionDecisionItem, DPObligations, DecisionType

CASE_LISTING_URL = "https://www.pdpc.gov.sg/api/pdpcenforcementcases/getenforcementcaselisting"


def create_form_data(page: int):
    return {
        "keyword": "",
        "industry": "all",
        "nature": "all",
        "decision": "all",
        "penalty": "all",
        "page": str(page)
    }


class CommissionDecisionSpider(scrapy.Spider):
    name = "PDPCCommissionDecisions"

    custom_settings = {
        "FILES_STORE": 'downloads',
    }

    def start_requests(self):
        default_form_data = {
            "keyword": "",
            "industry": "all",
            "nature": "all",
            "decision": "all",
            "penalty": "all",
            "page": "1"
        }

        response = requests.post(CASE_LISTING_URL, data=default_form_data)

        if response.status_code == requests.codes.ok:
            response_json = response.json()
            total_pages = response_json["totalPages"]

            for page in range(1, total_pages + 1):
                yield FormRequest(CASE_LISTING_URL, formdata=create_form_data(page=page))

    def parse(self, response, **kwargs):
        response_json = response.json()
        for item in response_json["items"]:
            self.logger.info(f'See item \"{item["title"]}\"')
            from datetime import datetime
            nature = [DPObligations(nature.strip()) for nature in item["nature"].split(',')] if item[
                "nature"] else "None"
            decision = [DecisionType(decision.strip()) for decision in item["decision"].split(',')] if item[
                "decision"] else "None"
            yield CommissionDecisionItem(
                title=item["title"],
                summary_url=f"https://www.pdpc.gov.sg{item['url']}",
                published_date=datetime.strptime(item["date"], '%d %b %Y'),
                nature=nature,
                decision=decision
            )
