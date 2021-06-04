import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    all_list = getAll()
    for a in all_list:
        # try:
            # print(a[0])# :idx
            # print(a[1])# :osp_id
            # print(a[2])# :domain
            # print(a[3])# :cp_id
            # print(a[4])# :cnt_id
            # print(a[5])# :title
            # print(a[6])# :craw_site_url
            # print(a[7])# :craw_url
            # print(a[8])# :craw_title_num

        # 키워드 체크
        getT = getTitle()
        titleCheck = checkTitle(a[5], getT)
        if titleCheck['m'] == None:
            # dbUpResult = dbNullUpdate(a[0])
            continue
        title = titleCheck['m']
        cp_id = titleCheck['i']
        cnt_id = titleCheck['k']
        title_null = titleNull(a[5])

        data = {
            'craw_osp_id': a[1],
            'craw_domain': a[2],
            'craw_cp_id': cp_id,
            'craw_cnt_id' : cnt_id,
            'craw_title': title,
            'craw_title_null': title_null,
            'craw_site_url' : a[6],
            'craw_url': a[7],
            'craw_title_num': a[8]
        }
        print(data)
        print("=================================")

            # dbResult = insertKeep(data)
            # dbUpResult = dbUpdate(cp_id,cnt_id,a[0])

        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()

    print("craw_keep 크롤링 시작")
    startCrawling()
    print("craw_keep 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
