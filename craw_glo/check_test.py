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
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;check = True;checkNum = 0
    # url = 'https://video.tudou.com/v/XMjk0MzEzOTEyOA==.html?from=s1.8-1-1.2'
    url = 'https://video.tudou.com/v/XNDAwMTE3ODM5Mg==.html?from=s1.8-1-1.2'
    try:
        print(url)
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('css/pc/common/404') != -1:
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

    print("check_test 재검수 시작")
    startCrawling()
    print("check_test 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
