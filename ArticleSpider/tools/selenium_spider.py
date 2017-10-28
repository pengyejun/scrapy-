from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import HtmlResponse


#设置chromedriver不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2} #设置为2表示不加载图片
chrome_opt.add_experimental_option("prefs", prefs)
browser=webdriver.Chrome(executable_path="H:\selenium_driver\chrome\chromedriver.exe",chrome_options=chrome_opt)
browser.get("https://chengdu.anjuke.com/community/tainfuxinqu/")
browser.quit()


#登录知乎
browser.get("https://www.zhihu.com/#signin")
browser.find_element_by_css_selector(".qrcode-signin-step1 span.signin-switch-password").click()
browser.find_element_by_css_selector(".view-signin input[name='account']").send_keys("15281826276")
browser.find_element_by_css_selector(".view-signin input[name='password']").send_keys("peng2664231")
browser.find_element_by_css_selector(".view-signin button.sign-button").click()


#拉勾登录
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2} #设置为2表示不加载图片
chrome_opt.add_experimental_option("prefs", prefs)
browser=webdriver.Chrome(executable_path="H:\selenium_driver\chrome\chromedriver.exe",chrome_options=chrome_opt)
browser.get("https://passport.lagou.com/login/login.html")
import time
time.sleep(5)
browser.find_element_by_css_selector("form.active > div[data-propertyname='username'] input").send_keys("15281826276")
browser.find_element_by_css_selector("form.active > div[data-propertyname='password'] input").send_keys("peng2664231")
browser.find_element_by_css_selector("form.active > div[data-propertyname='submit'] input").click()
