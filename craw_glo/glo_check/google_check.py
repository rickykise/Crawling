import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(url, chekc_item):
    i = 0;check = True;checkNum = 0
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # checkDate = chekc_item[0]
    # limitDate = str(chekc_item[0]  + timedelta(30))
    # if now < limitDate:
    # url = 'https://www.torrentrue.com/bbs/board.php?bo_table=kr_drama&wr_id=52524'
    try:
        link = 'https://www.google.com/search?q='+url
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        if text.find('삭제했습니다') != -1:
            checkNum = 1
            dbUpdate(checkNum,now,url)
        else:
            dbUpdate(checkNum,now,url)
    except:
        checkNum = 1
        dbUpdate(checkNum,now,url)

if __name__=='__main__':
    start_time = time.time()
    getUrl = getGoogleHostUrl()

    print("구글 재검수 크롤링 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("구글 재검수 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
