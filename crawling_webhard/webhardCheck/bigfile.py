import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'NSHcookie=20111006b0a72d26c6f0003; bAdult=N; _ga=GA1.3.13042308.1573712778; _gid=GA1.3.1914932234.1573712778; _gat=1',
    'Host': 'www.bigfile.co.kr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True; cnt_chk = 0
    url = "http://www.bigfile.co.kr"
    try:
        r = requests.get(url, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('title'):
            title = soup.find('title').text.strip()
            if title.find('Bad Gateway') != -1:
                cnt_chk = 1
            data = {
                'Cnt_osp' : 'bigfile',
                'Cnt_url': url,
                'Cnt_chk': cnt_chk
            }
            dbResult = insertALL(data)
    except:
        cnt_chk = 1
        data = {
            'Cnt_osp' : 'bigfile',
            'Cnt_url': url,
            'Cnt_chk': cnt_chk
        }
        dbResult = insertALL(data)

if __name__=='__main__':
    start_time = time.time()

    print("bigfile 크롤링 시작")
    startCrawling()
    print("bigfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
