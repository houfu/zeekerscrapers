import scrapy.pipelines.files
from itemadapter import ItemAdapter
from scrapy import Request


class ZeekerDownloadFilePipeline(scrapy.pipelines.files.FilesPipeline):

    def file_path(self, request: Request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return f"{request.meta['zeeker']}/{adapter['published_date']} {adapter['neutral_citation']}.pdf" \
            if item else None
