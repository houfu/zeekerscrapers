# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

import bs4
import requests
import scrapy.pipelines.files
from itemadapter import ItemAdapter


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


class PDPCDecisionDownloadFilePipeline(scrapy.pipelines.files.FilesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return f"full/{adapter['title']}.pdf" if item else None
