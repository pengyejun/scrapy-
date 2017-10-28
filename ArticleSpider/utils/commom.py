# -*- coding: utf-8 -*-

import hashlib
import re
import datetime
def get_md5(url):
    if isinstance(url,str):
        url=url.encode("utf-8")
    m=hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums
def get_html_num(value):
    match_obj=re.match(r".*,(\d+).html",value)
    if match_obj:
        nums=int(match_obj.group(1))
    else:
        nums=0
    return nums
def date_convert(value):
    try:
        # 处理日期
        creat_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        creat_date = datetime.datetime.now().date()
    return creat_date
# if __name__=="__main__":
#     print(get_md5("peng"))


# class A(object):
#     def __init__(self):
#         print("enter A")
#         super(A, self).__init__()  # new
#         print("leave A")
#
#
# class B(object):
#     def __init__(self):
#         print("enter B")
#         super(B, self).__init__()  # new
#         print("leave B")
#
#
# class C(A):
#     def __init__(self):
#         print("enter C")
#         super(C, self).__init__()
#         print("leave C")
#
#
# class D(A):
#     def __init__(self):
#         print("enter D")
#         super(D, self).__init__()
#         print("leave D")
#
#
# class E(B, C):
#     def __init__(self):
#         print("enter E")
#         super(E, self).__init__()  # change
#         print ("leave E")
#
#
# class F(E, D):
#     def __init__(self):
#         print("enter F")
#         super(F, self).__init__()  # change
#         print("leave F")
# print(F.__mro__)
# f=F()




