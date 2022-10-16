import datetime

import pytest
import requests

from pdpcSpider.spiders.CommissionDecisionSpider import CASE_LISTING_URL, CommissionDecisionSpider
from pdpcSpider.spiders.CommissionDecisionSpider import create_form_data


@pytest.mark.vcr
def test_start_url():
    response = requests.post(CASE_LISTING_URL, data=create_form_data(1))
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["ResponseCode"] == "OK"


@pytest.mark.default_cassette("test_start_url.yaml")
@pytest.mark.vcr
def test_parse():
    response = requests.post(CASE_LISTING_URL, data=create_form_data(1))
    spider = CommissionDecisionSpider()
    from scrapy.http import TextResponse
    results = spider.parse(TextResponse(url="", body=response.content))
    test = next(results)
    assert test.title == "Breach of the Protection Obligation by Crawfort"
    assert test.published_date == "14 Jul 2022"
    assert test.summary_url == "https://www.pdpc.gov.sg/all-commissions-decisions/2022/07/" \
                               "breach-of-the-protection-obligation-by-crawfort"
    from pdpcSpider.items import DPObligations
    assert test.nature == [DPObligations.PROTECTION]
    from pdpcSpider.items import DecisionType
    assert test.decision == [DecisionType.DIRECTIONS]
