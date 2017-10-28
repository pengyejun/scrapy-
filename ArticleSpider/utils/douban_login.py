# -*- coding: utf-8 -*-
import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import os
try:
    from PIL import Image
except:
    pass


# 构造 Request headers
agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
headers = {
    "Host": "www.douban.com",
    "Referer": "https://www.douban.com/",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except:
    print("Cookie 未能加载")


def get_xsrf():
    response=session.get("https://www.zhihu.com",headers=headers)
    match_obj=re.match('.*name="_xsrf" value="(.*?)"', response.text,re.DOTALL)
    if match_obj:
        return match_obj.group(1)
    else:
        return ""


# 获取验证码
def get_captcha(captcha_url):
    r = session.get(captcha_url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.douban.com/people/166800915/"
    login_code = session.get(url, headers=headers, allow_redirects=False).status_code
    if login_code == 200:
        print(True)
        return True
    else:
        print(False)
        return False


def login(account, passwd):
    post_url="https://accounts.douban.com/login"
    post_data={
        "source":"None",
        "redir":"https://www.douban.com",
        "form_email":account,
        "form_password":passwd,
        "login":"登录"
    }
    # 不需要验证码直接登录成功
    login_page = session.post(post_url, data=post_data, headers=headers)
    if  isLogin() == False:
        # 不输入验证码登录失败
        # 使用需要输入验证码的方式登录
        print("登录失败")
        login_page = session.get("https://www.douban.com", headers=headers)
        match_obj=re.match('.*id="captcha_image" src="(.*?)".*',login_page.text,re.DOTALL)
        match_obj1 = re.match('.*name="captcha-id" value="(.*?)".*', login_page.text, re.DOTALL)
        post_data["captcha-id"] = match_obj1.group(1)
        yz_url=match_obj.group(1)
        post_data["captcha-solution"] = get_captcha(yz_url)
        login_page = session.post(post_url, data=post_data, headers=headers)
        # login_code = login_page.json()
        # print(login_code['msg'])
    # 保存 cookies 到文件，
    # 下次可以使用 cookie 直接登录，不需要输入账号和密码
    isLogin()
    session.cookies.save()
    isLogin()


if __name__ == '__main__':
    if isLogin():
        print('您已经登录')
    else:
        login("xxx", "xxx")