# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItemLoader,LagouJobItem

class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/chengdu']

    headers = {
        "HOST": "passport.lagou.com",
        "Referer": "https://www.lagou.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    }

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name span::text")
        item_loader.add_value("url", response.url)
        item_loader.add_css("salary", ".salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")

        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div > p")
        item_loader.add_css("job_addr", ".work_addr")

        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_css("company_name", "#job_company dt a div h2::text")

        job_item = item_loader.load_item()

        return job_item




