# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import json
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import Anjuke_xiaoqu,AriticleItemloader
from fake_useragent import UserAgent

class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['chengdu.anjuke.com']
    start_urls = ['https://chengdu.anjuke.com/community/']

    agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    headers = {
        "HOST": "login.anjuke.com",
        "Referer": "https://chengdu.anjuke.com/",
        "User-Agent": agent
    }
    def parse(self, response):
        page_urls=response.css(".items-list .items:first-child span.elems-l a::attr(href)").extract()
        for page_url in page_urls[1:]:
            yield Request(url=page_url,callback=self.parse_page)

    def parse_page(self, response):
        post_nodes=response.css("#list-content > div.li-itemmod")
        for post_node in post_nodes:
            post_url=post_node.css("a.img::attr(href)").extract()[0]
            price=post_node.css(".li-side strong::text").extract()[0]
            price_ratio=post_node.css(".li-side .price-txt::text").extract()[0]
            addr=post_node.css(".li-info address::text").extract()[0].strip()
            built_years=post_node.css(".li-info .date::text").extract()[0].strip()

            yield Request(url=parse.urljoin(response.url,post_url),meta={"price":price,"price_ratio":price_ratio,"addr":addr,"built_years":built_years},callback=self.paser_detail)

        next_url=response.css(".aNxt::attr(href)").extract()[0]
        if next_url:
            yield Request(url=next_url,callback=self.parse_page)

    custom_settings = {
        'DOWNLOAD_DELAY' : 10,
    }
    def paser_detail(self,response):
        match_obj=re.match(r".*community/view/?(\d+).*",response.url)
        if match_obj:
            ua=UserAgent()
            headers = {"User-Agent": ua.random}
            id = match_obj.group(1)
            url_cnt = "https://chengdu.anjuke.com/v3/ajax/communityext/?commid={0}&useflg=onlyForAjax".format(id)
            cnt_re=requests.get(url_cnt,headers=headers)
            cnt_json=json.loads(cnt_re.text)
            sale_cnt=cnt_json["comm_propnum"]["saleNum"]
            rent_cnt = cnt_json["comm_propnum"]["rentNum"]
        price=response.meta.get("price","")
        price_ratio=response.meta.get("price_ratio","")
        addr=response.meta.get("addr","")
        built_years=response.meta.get("built_years","")
        item_load=AriticleItemloader(item=Anjuke_xiaoqu(),response=response)
        item_load.add_value("price",price)
        item_load.add_value("price_ratio", price_ratio)
        item_load.add_value("addr", addr)
        item_load.add_value("built_years", built_years)
        item_load.add_css("title",".comm-title h1::text")
        item_load.add_value("title_url",response.url)
        item_load.add_value("rent_cnt", rent_cnt)
        item_load.add_value("sale_cnt", sale_cnt)
        item_load.add_css("use_type","#basic-infos-box > dl > dd:nth-child(2)::text")
        item_load.add_css("construct_area","#basic-infos-box > dl > dd:nth-child(6)::text")
        item_load.add_css("built_years","#basic-infos-box > dl > dd:nth-child(10)::text")
        item_load.add_css("volume_ratio","#basic-infos-box > dl > dd:nth-child(14)::text")
        item_load.add_css("kf_company","#basic-infos-box > dl > dd:nth-child(18)::text")
        item_load.add_css("wy_company","#basic-infos-box > dl > dd:nth-child(20)::text")
        item_load.add_css("wy_fee","#basic-infos-box > dl > dd:nth-child(4)::text")
        item_load.add_css("house_cnt","#basic-infos-box > dl > dd:nth-child(8)::text")
        item_load.add_css("park_cnt","#basic-infos-box > dl > dd:nth-child(12)::text")
        item_load.add_css("green_ratio","#basic-infos-box > dl > dd:nth-child(16)::text")

        Anjuke_Item=item_load.load_item()

        yield Anjuke_Item

















