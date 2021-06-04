import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *

cnt_osp = 'filerun'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            cnt_chk = 0
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            if text.find('삭제된 컨텐츠입니다') != -1:
                cnt_chk = 2
        except:
            cnt_chk = 2

        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("filerun check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filerun check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
