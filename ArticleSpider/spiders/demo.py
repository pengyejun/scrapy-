# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import Dongfangcaifu

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['money.eastmoney.com'] #finance.eastmoney.com
    start_urls = ['http://money.eastmoney.com/news/clczx.html/']
    #http://money.eastmoney.com/news/clczx.html/
    #http://finance.eastmoney.com/news/cgsxw.html/

    def parse(self, response):
        page_urls=response.css("#newsListContent  a::attr(href)").extract()
        for page_url in page_urls:
            yield Request(url=parse.urljoin(response.url,page_url),callback=self.paser_detail)

        next_url=response.css("#pagerNoDiv > a:nth-last-child(1)").extract()[0]
        if '下一页' in next_url:
            next_page=response.css("#pagerNoDiv > a:nth-last-child(1)::attr(href)").extract()[0]
            yield Request(url=parse.urljoin("http://money.eastmoney.com/news/",next_page),callback=self.parse) #http://finance.eastmoney.com/news/

    custom_settings = {
        'DOWNLOAD_DELAY': 5,
    }

    def paser_detail(self,response):
        item=Dongfangcaifu()
        url=response.url
        title=response.css(".newsContent h1::text").extract()[0]
        publish_time=response.css(".time-source > .time::text").extract()[0]
        source=response.css(".time-source > .source > img::attr(alt)").extract()
        edit=response.css(".time-source > span > a::text").extract()
        if edit:
            edit=edit[0]
        else:
            edit='暂无数据'
        if source:
            source=source[0]
        else:
            source='暂无数据'
        content = ''.join(response.css("#ContentBody > p").xpath("string(.)").extract())
        content=content.split()[:-1]
        content=''.join(content)
        item["url"]=url
        item["title"]=title
        item["publish_time"]=publish_time
        item["source"]=source
        item["edit"]=edit
        item["content"]=content
        yield item




