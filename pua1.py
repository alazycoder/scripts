# -*- coding:utf-8 –*-
import requests
from bs4 import BeautifulSoup
import sys
import re
import os


# 获取html代码
def getHTMLText(url):
    r = requests.get(url, timeout=100)
    while (r.status_code != 200):
        r = requests.get(url, timeout=100)
    r.encoding = r.apparent_encoding
    return r.text


# 从leftmenu找到所有模块入口
def getLeftMenu():
    text = getHTMLText('http://www.puahome.com/')
    soup = BeautifulSoup(text, "html.parser")
    leftmenu = soup.find(class_='leftmenu')
    p = re.compile('http.*?<')
    mylist = re.findall(p, leftmenu.__str__())
    for i in range(len(mylist)):
        mylist[i] = mylist[i][0:mylist[i].__len__() - 1]
    tmp = sorted(list(set(mylist)), key=mylist.index)
    return tmp


# 找到当前页面包含的所有 pua-****。html
def getArticleList(url):
    text = getHTMLText(url)
    soup = BeautifulSoup(text, "html.parser")
    p = re.compile('pua-.*?</em>')
    mylist = re.findall(p, soup.__str__())
    return sorted(list(set(mylist)), key=mylist.index)


# 获得最大页数
def getMaxPageNumber(url):
    maxPageNumber = 1
    text = getHTMLText(url)
    soup = BeautifulSoup(text, "html.parser")
    pg = soup.find_all(class_='pg')
    if (pg.__len__() != 0):
        p = re.compile('f-.*?html')
        list = re.findall(p, pg.__str__())
        for x in list:
            tmp = re.split('-|\.', x)
            maxPageNumber = max(maxPageNumber, int(tmp[2]))
    return maxPageNumber


# 处理html代码
def filter_tags(htmlstr):
    re_img = re.compile('<ignore_js_op>[\s\S]*?</ignore_js_op>')  # 处理图片
    s = re_img.sub('', htmlstr)  # 去掉图片
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    s = re_cdata.sub('', s)  # 去掉CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    s = re_script.sub('', s)  # 去掉SCRIPT
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    s = re_style.sub('', s)  # 去掉style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    s = re_br.sub('\n', s)  # 将br转换为换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    s = re_h.sub('', s)  # 去掉HTML 标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_comment.sub('', s)  # 去掉HTML注释
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    return s


def cleanHtml(text):
    re_img = re.compile('<ignore_js_op>[\s\S]*?</ignore_js_op>')  # 处理图片
    text = re_img.sub('', text.__str__())  # 去掉图片
    re_img = re.compile('#weixin#')  # 处理广告
    text = re_img.sub('', text.__str__())  # 去掉广告
    re_status = re.compile('<i class="pstatus">[\s\S]*?</i>')  # 处理图片
    text = re_status.sub('', text.__str__())  # 去掉图片
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    text = re_br.sub('', text.__str__())  # 删除空行
    # blank_line = re.compile('\s')  #删除所有空白字符
    # text = blank_line.sub('', text.__str__())
    blank_line = re.compile('\n+')
    text = blank_line.sub('\n', text.__str__())
    newsoup = BeautifulSoup(text.__str__(), "html.parser")
    return newsoup.get_text().__str__()


def getArtile(url, type, replyNum, clickNum):
    text = getHTMLText(url)
    soup = BeautifulSoup(text, "html.parser")
    title = soup.head.title.text
    title = title.replace(' ', '')
    # title：恋爱秘籍：如何掌握在微信上与女生聊天的技巧？-聊天技巧-PUA论坛
    title = title.split('-')[0].encode('utf-8')
    # 文章按title去重
    if (title in allArticle):
        return
    allArticle.add(title)
    type = type.encode('utf-8')
    if (allType.has_key(type) == False):
        allType[type] = 0
        path = 'data\\' + type
        path = path.encode('gbk')  # 中文路径
        if (os.path.exists(path) == False):
            os.mkdir(path)
    id = allType[type]
    allType[type] = allType[type] + 1
    print url
    print "id= " + str(id)
    path = "data\\" + type + "\\" + str(id) + ".txt"
    path = path.encode('gbk')  # 中文路径
    text = soup.find(class_="t_f")
    text = cleanHtml(text)
    file = open(path, "w")
    file.write(url + "\n")
    file.write("[题目]" + title.encode('utf-8') + '\n')
    file.write("[回复]" + str(replyNum) + '\n')
    file.write("[查看]" + str(clickNum) + '\n')
    file.write("[正文]\n")
    file.write(text.encode('utf-8'))
    file.close()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if (os.path.exists('data') == False):
        os.mkdir('data')
    global allType
    allType = {}
    global allArticle
    allArticle = set()

    entrance = getLeftMenu()
    # 讨论区
    for i in range(4, 34):
        pageUrl = entrance[i].split('">')[0]
        type = entrance[i].split('">')[1]
        print type + str(i)
        maxPageNumber = getMaxPageNumber(pageUrl)
        for j in range(1, maxPageNumber + 1):
            s = pageUrl
            old = '1.html'
            new = j.__str__() + '.html'
            s = s.replace(old, new)
            # print "************" + s
            articleList = getArticleList(s)
            for s in articleList:
                tmp = s.split('"')
                realUrl = "http://www.puahome.com/bbs/" + tmp[0]
                m = re.findall(r'(\w*[0-9]+)\w*', tmp[1])
                try:
                    getArtile(realUrl, type, m[0], m[1])
                except:
                    print "here run failed " + s
