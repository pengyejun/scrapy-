# -*- coding: utf-8 -*-
__author__ = 'bobby'
import requests
from scrapy.selector import Selector
import MySQLdb
import time

from fake_useragent import UserAgent

conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="p12345", db="test", charset="utf8")
cursor = conn.cursor()


def crawl_ips():
    #爬取西刺的免费ip代理
    ua = UserAgent()
    for i in range(1,1000):
        headers = {"User-Agent": ua.random}
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
        time.sleep(10)
        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")


        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = float(speed_str.split("秒")[0])
            if speed >= 4.0:
                continue
            all_texts = tr.css("td::text").extract()

            ip = all_texts[0]
            port = all_texts[1]
            proxy_type=all_texts[5]
            ip_list.append((ip, port, speed, proxy_type))

        for ip_info in ip_list:
            cursor.execute(
                "insert into proxy_ip_http(ip, port, speed,proxy_type) VALUES('{0}', '{1}', '{2}','{3}') ON DUPLICATE KEY UPDATE port=VALUES(port)".format(
                    ip_info[0], ip_info[1], ip_info[2],ip_info[3]
                )
            )

            conn.commit()


class GetIP(object):
    def delete_ip(self, ip):
        #从数据库中删除无效的ip
        delete_sql = """
            delete from proxy_ip where ip='{0}'
        """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port,proxy_type):
        #判断ip是否可用
        http_url = "http://blog.jobbole.com/all-posts/"
        proxy_url = "{2}://{0}:{1}".format(ip, port,proxy_type)
        try:
            proxy_dict = {
                "{0}".format(proxy_type):proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print ("invalid ip and port")
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                print  ("invalid ip and port")
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        #从数据库中随机获取一个可用的ip
        random_sql = """
              SELECT ip, port, proxy_type FROM proxy_ip
            ORDER BY RAND()
            LIMIT 1
            """
        result = cursor.execute(random_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type=ip_info[2]

            judge_re = self.judge_ip(ip, port,proxy_type)
            if judge_re:
                return "{2}://{0}:{1}".format(ip, port,proxy_type)
            else:
                return self.get_random_ip()



# crawl_ips()
if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()