#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf8')

myrank = 6700  # rank in your province


def is_num_by_except(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"


def solve(id, school):
    # print school
    ok = 0
    url = "https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=8306&format=json&ie=utf-8&oe=utf-8&query="
    url += school
    url += "&from_mid=1&tn=tangram&province=北京&curriculum=理科&batch=一批&_=1498367050903&cb=jsonp3"
    r = requests.get(url)
    x = r.text.split("\"")
    for i in range(len(x)):
        if (x[i] == "precedence"):
            if (is_num_by_except(x[i + 2])):
                if (abs(int(x[i + 2]) - myrank) < 500):
                    ok = ok + 1
    if (ok > 1):
        # f=open("result.txt","w")
        print  school + "（排名 " + str(id) + " ）: 近6年有 " + str(ok) + " 年平均录取排名在6200-7200名之间"
        # f.write(str(id) + "  "+ school)
        # f.close()


if __name__ == "__main__":
    url1 = "https://m.baidu.com/sf?pd=education_kg&openapi=1&dspName=iphone&from_sf=1&pn="
    url2 = "&rn=10&resource_id=4534&top=%7B%22sfhs%22%3A12%7D&word=%E5%A4%A7%E5%AD%A6%E6%8E%92%E5%90%8D&title=%E9%99%A2%E6%A0%A1%E5%88%97%E8%A1%A8&lid=11817669656565993169&ms=1&frsrcid=4551&frorder=1&province_name=%E5%8C%97%E4%BA%AC"
    j = 0
    for st in range(0, 500, 10):
        url = url1 + str(st) + url2
        demo = getHTMLText(url)
        soup = BeautifulSoup(demo, "html.parser")
        all = soup.find_all(class_="c-line-clamp1 c-color")
        for val in all:
            j = j + 1
            solve(j, val.get_text())
