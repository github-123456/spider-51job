import scrapy
from tutorial.items import *
from scrapy.selector import Selector
from scrapy import signals
import datetime


class SpiderPost(scrapy.Spider):
    name = "post"

    def __init__(self, urls, page_count, keys):
        self.urls = urls
        self.page_count = int(page_count)
        self.keys = keys
        self.invalid = 0
        self.page_index = 0
        print("maximum list page total count:", self.page_count)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url,
                self.parse)

    def parse(self, response):
        links = Selector(response).css(".p_in ul .bk a::attr(href)").extract()
        if links.__len__() == 0:
            next_page = None
        else:
            next_page = links[links.__len__() - 1]
        self.page_count = self.page_count - 1

        if self.page_count < 0:
            print("warn:page count upper limit exceeded,did not complete all scraping")
            return

        for i in response.css('.dw_table .el:not(.title)').extract():
            pi = PostItem.create(i, self.keys)
            if pi is None:
                self.invalid = self.invalid + 1
                print("found", self.invalid, "items dost not match key", self.keys)
        self.page_index = self.page_index + 1
        print("finished scraping page", self.page_index)
        if next_page is not None:
            yield scrapy.Request(next_page, self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SpiderPost, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        spider.logger.info('Spider closed: %s', spider.name)
        PostItem.save_excel(PostItem.instances,
                            "51job-data-" + datetime.datetime.now().strftime("%y%m%d-%H%M%S") + ".xlsx")
