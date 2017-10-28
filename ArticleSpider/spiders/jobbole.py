# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
import re
from ArticleSpider.items import ArticleItem,AriticleItemloader
from ArticleSpider.utils.commom import get_md5
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse
        """
        post_nodes=response.css("#archive > .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            img_url=post_node.css("img::attr(src)").extract()[0]
            post_url = post_node.css("::attr(href)").extract()[0]
            yield scrapy.Request(url=parse.urljoin(response.url,post_url),meta={"img_url":img_url},callback=self.parse_detail)

        #提取下一页并交给scrapy下载
        next_url=response.css(".next.page-numbers::attr(href)").extract()[0]
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)


    def parse_detail(self,response):
        # Aricle_item=ArticleItem()
        # #提取文章具体字段
        # title=response.xpath('//*[@class="entry-header"]/h1/text()').extract()[0]
        # #封面图
        img_url=response.meta.get("img_url","")
        # #css  response.css('div.entry-header > h1::text').extract()[0]
        # #css   response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·","").strip()
        # prise_count=response.css('.vote-post-up>h10::text').extract()[0]
        creat_date=response.css('p.entry-meta-hide-on-mobile::text').extract()[0].strip().replace("·","").strip()
        # collection_count = response.css('.bookmark-btn::text').extract()[0]
        # match=re.match(".*?(\d+).*",collection_count)
        # if match:
        #     collection_count=int(match.group(1))
        # else:
        #     collection_count=0
        # comments_num=response.css('.post-adds>a>span::text').extract()[0]
        # match1 = re.match(".*?(\d+).*", comments_num)
        # if match1:
        #     comments_num=int(match1.group(1))
        # else:
        #     comments_num=0
        # #css   response.css('.vote-post-up>h10::text').extract()[0]
        # #content=response.xpath('//*[@class="entry"]/p[2]/text()').extract()[0]
        # #css    response.css('#post-112351 > div.entry > p:nth-child(8)::text').extract()[0]
        tag_list=response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list=[x for x in tag_list if not re.match(".*评论.*",x)]  #正则提取不包含评论的标签
        tags=",".join(tag_list)
        #
        # Aricle_item["title"]=title
        # Aricle_item["url"]=response.url
        # Aricle_item["url_id"]=get_md5(response.url)
        # Aricle_item["prise_count"]=prise_count
        # Aricle_item["collection_count"]=collection_count
        # Aricle_item["comments_num"]=comments_num
        # Aricle_item["img_url"]=[img_url] ###
        # Aricle_item["tags"]=tags
        # try:
        #     #处理日期
        #     creat_date=datetime.datetime.strptime(creat_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     creat_date=datetime.datetime.now().date()
        # Aricle_item["creat_date"]=creat_date


        # 通过ItemLoader加载item
        item_loader=AriticleItemloader(item=ArticleItem(),response=response)
        item_loader.add_xpath("title",'//*[@class="entry-header"]/h1/text()')
        item_loader.add_css("prise_count",'.vote-post-up>h10::text')
        item_loader.add_css("collection_count", '.bookmark-btn::text')
        item_loader.add_css("comments_num", '.post-adds>a>span::text')
        item_loader.add_value("tags", tags)
        item_loader.add_value("creat_date",creat_date)
        item_loader.add_value("url_id", get_md5(response.url))
        item_loader.add_value("url",response.url)
        item_loader.add_value("img_url", [img_url])
        Aricle_item=item_loader.load_item()


        yield Aricle_item







