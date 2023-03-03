from scrapy import Selector
from scrapy.spiders import XMLFeedSpider

from stateCourtSpider.items import StateCourtDecisionItem


class LatestJudgmentsStateCourtSpider(XMLFeedSpider):
    def parse(self, response, **kwargs):
        super().parse(response, **kwargs)

    name = 'latestJudgmentsStateCourtSpider'
    allowed_domains = ['lawnet.sg']
    start_urls = [
        "https://www.lawnet.sg/lawnet/web/lawnet/free-resources?p_p_id=freeresources_WAR_lawnet3baseportlet"
        "&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=subordinateRSS&p_p_cacheability"
        "=cacheLevelPage&p_p_col_id=column-1&p_p_col_pos=2&p_p_col_count=3"
        "&_freeresources_WAR_lawnet3baseportlet_total=82"
    ]
    iterator = 'iternodes'
    itertag = 'item'
    custom_settings = {
        "FILES_STORE": 'downloads',
    }

    def parse_node(self, response, selector: Selector):
        raw_title = selector.xpath('title').get().split('-')
        item: StateCourtDecisionItem = StateCourtDecisionItem(
            title=raw_title[0].strip(),
            neutral_citation=raw_title[1].strip(),
            published_date=selector.xpath('pubDate').get(),
            file_urls=[selector.xpath('link').get()]
        )
        return item
