# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import re
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst
import datetime
from scrapy.loader import ItemLoader
from ArticleSpider.utils.commom import get_html_num
from ArticleSpider.utils.caclu_sentiment import caclu_sentiment


from ArticleSpider.utils.commom import get_nums,date_convert
from w3lib.html import remove_tags

class AriticleItemloader(ItemLoader):
    #自定义Itemloader
   default_output_processor = TakeFirst()

def return_value(value):
    return value

class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    url=scrapy.Field()
    url_id = scrapy.Field()
    prise_count=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    collection_count=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments_num=scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags=scrapy.Field(
    )
    img_url=scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    img_path=scrapy.Field()
    creat_date=scrapy.Field(
        input_processor=MapCompose(date_convert)
    )

    def get_insert_sql(self):
        insert_sql = """
            insert into jobbole_article(title, url, url_id, creat_date, img_url, img_path,
            prise_count, collection_count, comments_num, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE comments_num=VALUES(comments_num), collection_count=VALUES(collection_count), prise_count=VALUES(prise_count)
        """

        # image_url = ""
        # # content = remove_tags(self["content"])
        #
        # if self["image_url"]:
        #     image_url = self["image_url"][0]
        params = (self["title"], self["url"], self["url_id"], self["creat_date"], self["img_url"],
                  self["img_path"], self["prise_count"], self["collection_count"], self["comments_num"],
                  self["tags"])
        return insert_sql, params



def remove_split(value):
    #去除分隔线
    return value.split()

class Anjuke_xiaoqu(scrapy.Item):
    #安居客小区Item
    title = scrapy.Field(
        input_processor=MapCompose(remove_split)
    )
    title_url=scrapy.Field()
    use_type=scrapy.Field()
    price = scrapy.Field()
    price_ratio = scrapy.Field()
    addr = scrapy.Field()
    built_years = scrapy.Field()
    construct_area= scrapy.Field()
    volume_ratio= scrapy.Field()
    kf_company= scrapy.Field()
    wy_company= scrapy.Field()
    wy_fee= scrapy.Field()
    house_cnt= scrapy.Field()
    park_cnt= scrapy.Field()
    green_ratio= scrapy.Field()
    sale_cnt= scrapy.Field()
    rent_cnt= scrapy.Field()
    def get_insert_sql(self):
        insert_sql = """
            insert into anjuke_xiaoq(title, title_url, use_type, price, price_ratio, addr, built_years, construct_area, volume_ratio, kf_company, wy_company, wy_fee, house_cnt, park_cnt, green_ratio, sale_cnt, rent_cnt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE price=VALUES(price), price_ratio=VALUES(price_ratio), sale_cnt=VALUES(sale_cnt), rent_cnt=VALUES(rent_cnt)
        """

        params = (self["title"], self["title_url"], self["use_type"], self["price"], self["price_ratio"],
                  self["addr"], self["built_years"], self["construct_area"], self["volume_ratio"],
                  self["kf_company"],self["wy_company"], self["wy_fee"], self["house_cnt"], self["park_cnt"], self["green_ratio"],
                  self["sale_cnt"], self["rent_cnt"])
        return insert_sql, params

class ZhihuAnswerItem(scrapy.Item):
    #知乎的问题回答item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


class ZhihuQuestionItem(scrapy.Item):
    #知乎的问题 item
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comments_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()



def replace_splash(value):
    return value.replace("/", "")

def handle_strip(value):
    return value.strip()

def remove_flags(value):
    list1=[]
    for x in value:
        match_obj=re.match(".*>(.*)<.*",x)
        list1.append(match_obj.group(1))
    return "".join(list1)
def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)

class LagouJobItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    #拉勾网职位
    title = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    degree_need = scrapy.Field(
        input_processor=MapCompose(replace_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(handle_strip,remove_flags),
    )
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, handle_jobaddr),
    )
    company_name = scrapy.Field(
        input_processor=MapCompose(handle_strip),
    )
    company_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into lagou_job(title, url, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_url, company_name, job_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE job_desc=VALUES(job_desc)
        """

        job_id = get_nums(self["url"])
        params = (self["title"], self["url"], self["salary"], self["job_city"], self["work_years"], self["degree_need"],
                  self["job_type"], self["publish_time"], self["job_advantage"], self["job_desc"], self["job_addr"],
                  self["company_url"],
                  self["company_name"], job_id)

        return insert_sql, params




class Dongfangcaifu(scrapy.Item):
    url=scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    source = scrapy.Field()
    edit = scrapy.Field()
    content = scrapy.Field()



    def get_insert_sql(self):
        insert_sql = """
            insert into licai(url, title, publish_time, source, edit, content,url_id,affections)
            VALUES (%s, %s, %s, %s, %s, %s,%s,%s)  ON DUPLICATE KEY UPDATE title=VALUES(title)
        """
        affections=caclu_sentiment(self["title"],self["content"])
        url_id=get_html_num(self["url"])
        params = (self["url"], self["title"], self["publish_time"], self["source"], self["edit"], self["content"],url_id,affections)

        return insert_sql, params
