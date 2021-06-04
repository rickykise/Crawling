import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling():
    i = 0;check = True; cnt_chk = 0
    url = "http://daoki.com"
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        data = {
            'Cnt_osp' : 'daoki',
            'Cnt_url': url,
            'Cnt_chk': cnt_chk
        }
        dbResult = insertALL(data)
    except:
        cnt_chk = 1
        data = {
            'Cnt_osp' : 'daoki',
            'Cnt_url': url,
            'Cnt_chk': cnt_chk
        }
        dbResult = insertALL(data)

if __name__=='__main__':
    start_time = time.time()

    print("daoki 크롤링 시작")
    startCrawling()
    print("daoki 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
