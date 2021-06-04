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
    try:
        r = requests.get(url)
        urlState = r.status_code
        if urlState == 200:
            dbUpdatetest(checkNum,now,url)
        else:
            checkNum = 1
            dbUpdatetest(checkNum,now,url)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getHostUrltest()

    print("f_list 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("f_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
