import requests
from selenium import webdriver
from bs4 import BeautifulSoup


def get_html_by_requests(url):
    try:
        r = requests.get(url, timeout=30)  # 设置timeout
        r.raise_for_status()  # 如果状态不是200(ok)，引发HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "error"


def get_html_by_phantomjs(url):
    try:
        driver = webdriver.PhantomJS(executable_path="/Users/gaohongjie/phantomjs/bin/phantomjs")
        driver.get(url)
        return driver.page_source
    except:
        return "error"


def get_soup(url):
    page_source = get_html_by_phantomjs(url)
    soup = BeautifulSoup(page_source, "html.parser")
    return soup