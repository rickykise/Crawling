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
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    osp_id = chekc_item[0]
    try:
        r = requests.get(url)
        urlState = r.status_code
        print(urlState)
        print('============================')
        # if urlState != 404 or urlState == 520 or urlState == 503:
        #     ospUpdateback(osp_id)
        # else:
        #     ospUpdate(osp_id)
        if urlState == 200:
            ospUpdateback(osp_id)
        elif urlState == 520 or urlState == 503:
            ospUpdateback(osp_id)
        else:
            ospUpdate(now, osp_id )
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getOspUrl()

    print("osp_list 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("osp_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
