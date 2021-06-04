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
    limitDate = str(chekc_item[0]  + timedelta(30))
    if now < limitDate:
        try:
            url = 'https://video.tudou.com/v/XMjk0MjkxMjI2MA==.html?from=s1.8-1-1.2'
            print(url)
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            print(soup.find('title'))
            # text = str(soup)

            if soup.find('title').text.find('404') != -1:
                # checkNum = 1
                # dbUpdate(checkNum,now,url)
                print('404')
            else:
                # dbUpdate(checkNum,now,url)
                print('정상')
        except:
            pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getYoukuHostUrl()

    print("youku_list 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("youku_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
