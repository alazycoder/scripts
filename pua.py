# -*- coding:utf-8 –*-
import requests
from bs4 import BeautifulSoup
import sys
import re
import os

#获取html代码
def getHTMLText(url):
    r = requests.get(url, timeout=1000)
    while(r.status_code!=200):
        r = requests.get(url, timeout=1000)
    r.encoding = r.apparent_encoding
    return r.text

#获取beautiful soup
def getSoup(url):
    text = getHTMLText(url)
    soup = BeautifulSoup(text, "html.parser")
    return soup

# 从leftmenu找到所有模块入口
def getLeftMenu():
    soup=getSoup('http://www.puahome.com/')
    leftmenu = soup.find(class_='leftmenu')
    return leftmenu.find_all('a')

#获得最大页数
def getMaxPageNumber(url):
    soup = getSoup(url)
    bm_h = soup.find('a',{'class':'bm_h'})
    return int(bm_h['totalpage'] if bm_h else 1)

# 找到当前页面包含的所有article
def getArticleList(url):
    soup = getSoup(url)
    return soup.find_all('a',{'class':'s xst'})

def getArtile(type,url,title):
    #按文章url去重
    if(article_url.has_key(url)):
        return
    article_url[url]=True
    #文件按type分目录
    dirpath = './htmldata/' + type
    # dirpath = dirpath.encode('gbk')  #中文路径
    if(type_num.has_key(type)==False):
        type_num[type]=0
        if (os.path.exists(dirpath) == False):
            os.mkdir(dirpath)
    id = type_num[type]
    type_num[type]=type_num[type]+1
    print url,type,id
    soup = getSoup(url)
    text = soup.find(class_="t_f")
    text = cleanHtml(text)
    print text
    glances =  soup.find('span',{'class':'s1'}).text #浏览数
    comments = soup.find('span',{'class':'s2'}).text #评论数
    supports = soup.find('span',{'class':'s3'}).text #支持数
    collections = soup.find('span', {'class': 's4'}).text #收藏数
    filepath = "./htmldata/" + type + "/" + str(id) + ".txt"
    # filepath = filepath.encode('gbk') # 中文路径
    file = open(filepath, "w")
    file.write(url+"\n")
    file.write("[题目]" + title.encode('utf-8')+'\n')
    file.write("[浏览]" + str(glances) + '\n')
    file.write("[评论]" + str(comments) + '\n')
    file.write("[支持]" + str(supports) + '\n')
    file.write("[收藏]" + str(collections) + '\n')
    file.write("[正文]\n")
    file.write(text.encode('utf-8'))
    file.close()

#处理html代码
def cleanHtml(text):
    soup=BeautifulSoup(text.__str__(),'html.parser')
    for s in soup('img'):
        print '*****************\n',s,'&&&&&&&&&&&&&&\n'
        s.extract()
    return soup

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    global  article_url,type_num
    article_url={}
    type_num={}
    if (os.path.exists('htmldata') == False):
        os.mkdir('htmldata')
    entrance = getLeftMenu()
    for i in range(3,36):
        item=entrance[i]
        pageUrl=item['href']
        type=item.text
        if(pageUrl.find('javascript')!=-1):
            continue
        maxPageNumber = getMaxPageNumber(pageUrl)
        #print i,pageUrl,type,maxPageNumber
        for j in range(1, maxPageNumber + 1):
            s = pageUrl
            old = '1.html'
            new = j.__str__() + '.html'
            s = s.replace(old, new)
            articleList = getArticleList(s)
            for s in articleList:
                tmp= s['href']
                realUrl= "http://www.puahome.com/bbs/"+tmp
                try:
                   getArtile(type,realUrl,s.text)
                except:
                    print "failed : " + realUrl
                exit()