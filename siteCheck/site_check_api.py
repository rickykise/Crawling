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
from checkFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(host_url, chekc_item):
    i = 0;check = True;checkNum = 0;chUrl="";reUrl="";cnt_id=chekc_item[1]
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    checkDate = chekc_item[0]
    limitDate = str(chekc_item[0]  + timedelta(30))
    # if now < limitDate:
    try:
        checkNum = ospCheck(cnt_id,host_url)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        dbUpdate(checkNum,now,host_url)

        # print(cnt_id)
        # print(host_url)
        # print(checkNum)
        # print("=================================")
    except:
        pass


if __name__=='__main__':
    start_time = time.time()
    getUrl = getHostUrl()

    print("check_api 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("check_api 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
