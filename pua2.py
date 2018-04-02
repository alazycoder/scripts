# -*- coding:utf-8 –*-
import requests
from bs4 import BeautifulSoup
import sys
import re
import os


#获取html代码
def getHTMLText(url):
    r = requests.get(url, timeout=100)
    while(r.status_code!=200):
        r = requests.get(url, timeout=100)
    r.encoding = r.apparent_encoding
    return r.text

def cleanHtml(text):
    soup = BeautifulSoup(text.__str__(), "html.parser")
    newtext=soup.get_text()
    blank_line = re.compile('\n+')
    newtext = blank_line.sub('\n', newtext.__str__())
    last_line = re.compile('Tagged with[.]*.*$')  #去掉文章最后一行
    newtext = last_line.sub('',newtext.__str__())
    return newtext


def getFile(dir,url):
    file = open(dir + '\\' + str(num) + '.txt', "w")
    text = getHTMLText(url)
    soup = BeautifulSoup(text, 'html.parser')
    title = soup.find('h1',{'class':'entry-title'}).text
    content = soup.find('div',{'class':'entry_content'})
    content = cleanHtml(content)
    file.write(url + "\n")
    file.write("[题目]" + title.encode('utf-8') + '\n')
    file.write("[回复]"  + '0\n')
    file.write("[查看]" + '0\n')
    file.write("[正文]\n")
    file.write(content.encode('utf-8'))
    file.close()



if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    global num
    num=0

    url='http://liaoshenme.puahome.com'
    urllist=list()

    folder = url[7:len(url)]

    if (os.path.exists(folder) == False):
        os.mkdir(folder)

    file=re.compile(url + r'/[0-9]{4}$')
    dir=re.compile(url + r'/category/[\S]+')

    text=getHTMLText(url)
    soup=BeautifulSoup(text,'html.parser')
    alist=soup.find_all('a',{'href':re.compile(url+'[\S]+')})
    for item in alist:
        aurl=item['href']
        if(dir.match(aurl)):
            newtext=getHTMLText(aurl)
            newsoup = BeautifulSoup(newtext, 'html.parser')
            newalist = newsoup.find_all('a',{'href':file})
            for i in newalist:
                urllist.append(i['href'])

    urllist=sorted(list(set(urllist)),key=urllist.index)

    for i in urllist:
        try:
            getFile(folder,i)
            num=num+1
        except:
            print 'failed : ' + i
    print str(num) + ' succeed !'