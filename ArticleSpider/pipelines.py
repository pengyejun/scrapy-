# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

import codecs
import json

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExporterPipeline(object):
    #调用scrapy提供的JsonItemExporter导出json文件
    def __init__(self):
        self.file=open('articleexport.json','wb')
        self.exporter=JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.exporter.start_exporting()


    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
# class JsonWithEncodingPipeline(object):
#     def __init__(self):
#         self.file=codecs.open('article.json','w',encoding="utf-8")
#
#     def process_item(self, item, spider):
#         lines=json.dumps(dict(item), ensure_ascii=False) + "\n"
#         self.file.write(lines)

    #     return item
    # def spider_closed(self,spider):
    #     self.file.close()
class ArticleimagePipeline(ImagesPipeline):

    def item_completed(self, results, item, info):

        for ok,value in results:
            if ok is True:
                img_path=value["path"]
        item["img_path"]=img_path
        return item



class MysqlPipeline(object):
    #采用同步的机制写入mysql

    def __init__(self):
        # self.conn=MySQLdb.connect('host','user','password','dbname',charset="utf8",use_unicode=True)
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'p12345', 'test', charset="utf8", use_unicode=True)
        self.cursor=self.conn.cursor()


    def process_item(self, item, spider):
        insert_sql="""
            insert into jobbole_article(title, url, url_id, creat_date, img_url, img_path, prise_count, collection_count, comments_num, tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_id"], item["creat_date"], item["img_url"], item["img_path"], item["prise_count"], item["collection_count"], item["comments_num"], item["tags"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbprams=dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )

        dbpool = adbapi.ConnectionPool("MySQLdb",**dbprams)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)  #处理异常

    def handle_error(self,failure):
        #处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

