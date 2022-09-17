from scrapy.spiders import XMLFeedSpider


class LatestJudgmentsStateCourtSpider(XMLFeedSpider):
    def parse(self, response, **kwargs):
        super().parse(response, **kwargs)

    name = 'latestJudgmentsStateCourtSpider'
    allowed_domains = ['lawnet.sg']
    start_urls = [
        "https://www.lawnet.sg/lawnet/web/lawnet/free-resources?p_p_id=freeresources_WAR_lawnet3baseportlet"
        "&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=subordinateRSS&p_p_cacheability"
        "=cacheLevelPage&p_p_col_id=column-1&p_p_col_pos=2&p_p_col_count=3"
        "&_freeresources_WAR_lawnet3baseportlet_total=82 "
    ]
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, selector):
        item = {}
        # item['url'] = selector.select('url').get()
        # item['name'] = selector.select('name').get()
        # item['description'] = selector.select('description').get()
        return item
