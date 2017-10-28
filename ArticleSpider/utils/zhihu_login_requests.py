# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import scrapy
import re

session = requests.session()
session.cookies=cookielib.LWPCookieJar(filename="cookie.txt")
try:
    session.cookies.load(ignore_discard=True)
    print("cookie加载成功")
except:
    print ("cookie未能加载")
agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
headers={
    "HOST":"www.zhihu.com",
    "Referer":"https://www.zhihu.com/?next=%2Finbox",
    "User-Agent":agent
}
def is_login():
    #通过个人中心页面返回状态码来判断是否为登录状态
    inbox_url="https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=headers,allow_redirects=False)
    if response.status_code == 200:
        print(True)
    else:
        print(False)


def get_index():
    response=session.get("https://www.zhihu.com",headers=headers)
    with open("index_page.html","wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def get_xsrf():
    response=session.get("https://www.zhihu.com",headers=headers)
    match_obj=re.match('.*name="_xsrf" value="(.*?)"', response.text,re.DOTALL)  #匹配失败
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


def zhihu_login(account,passwd):
    if re.match("1\d{10}",account):
        print("手机号登录")
        post_url="https://www.zhihu.com/login/phone_num"
        post_data={
            "_xsrf":get_xsrf(),
            "phone_num":account,
            "password":passwd,
            "captcha_type":"cn"
        }
    else:
        if "@" in account:
            #判断邮箱登录
            print("邮箱登录")
            post_url = "https://www.zhihu.com/login/email"
            post_data = {
                "_xsrf": get_xsrf(),
                "email": account,
                "password": passwd
            }
    response_text=session.post(post_url,data=post_data,headers=headers)
    session.cookies.save()            #验证码?

zhihu_login("xxx","xxx")
is_login()
# get_index()






