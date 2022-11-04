# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

import bs4
import requests
from itemadapter import ItemAdapter
from sqlmodel import Session

from common.ZeekerDownloadFilePipeline import ZeekerDownloadFilePipeline
from pdpcSpider.items import CommissionDecisionItem


class CommissionDecisionSummaryPagePipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        soup = bs4.BeautifulSoup(requests.get(adapter["summary_url"]).text, features="html5lib")
        article = soup.find('article')

        # Gets the summary from the decision summary page
        paragraphs = article.find(class_='rte').find_all('p')
        result = ''
        for paragraph in paragraphs:
            if not paragraph.text == '':
                result += re.sub(r'\s+', ' ', paragraph.text)
                break
        adapter["summary"] = result

        # Gets the respondent in the decision
        adapter["respondent"] = re.split(r"\s+[bB]y|[Aa]gainst\s+", article.find('h2').text, re.I)[1].strip()

        # Gets the link to the file to download the PDF decision
        decision_link = article.find('a')
        adapter["decision_url"] = f"https://www.pdpc.gov.sg{decision_link['href']}"

        adapter["file_urls"] = [f"https://www.pdpc.gov.sg{decision_link['href']}"]

        return item


class PDPCDecisionDownloadFilePipeline(ZeekerDownloadFilePipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return f"full/{adapter['published_date']} {adapter['title']}.pdf" if item else None


class PDPCDecisionAddToSQLPipeline:

    def __init__(self):
        from common.init_db import engine
        self.engine = engine

    def open_spider(self, spider):
        from pdpcSpider.models import CommissionDecisionModel, DecisionTypeModel, DecisionTypeLink, \
            DPObligationsModel, DPObligationsLink, create_DPObligations, create_DecisionType
        from common.init_db import create_db_and_tables
        create_db_and_tables()
        create_DPObligations()
        create_DecisionType()

    def process_item(self, item: CommissionDecisionItem, spider):
        with Session(self.engine) as session:
            from pdpcSpider.models import CommissionDecisionModel, DecisionTypeModel, DPObligationsModel
            decision = CommissionDecisionModel(
                neutral_citation=item.neutral_citation,
                title=item.title,
                published_date=item.published_date,
                summary_url=item.summary_url,
                respondent=item.respondent,
                decision_url=item.decision_url,
                summary=item.summary,
                decision=[DecisionTypeModel(value=decision) for decision in item.decision],
                nature=[DPObligationsModel(value=obligation) for obligation in item.nature]
            )
            session.add(decision)
            session.commit()
        return item


class PDPCDecisionDropDuplicatesPipeline:

    def __init__(self):
        from common.init_db import engine
        self.engine = engine
        self.lookup_table = []

    def open_spider(self, spider):
        from pdpcSpider.models import CommissionDecisionModel
        with Session(self.engine) as session:
            from sqlmodel import select
            results = session.exec(select(CommissionDecisionModel))
            for decision in results:
                self.lookup_table.append(decision.summary_url)

    def process_item(self, item: CommissionDecisionItem, spider):
        if item.summary_url in self.lookup_table:
            from scrapy.exceptions import DropItem
            raise DropItem(f"Decision {item.title} is already in database. Skip.")
        else:
            return item
