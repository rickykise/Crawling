import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    a = 1; b = 1
    headers = {
        'X-LZ-Locale' : 'ko-KR'
    }
    link = 'https://www.lezhin.com/api/v2/inventory_groups/home_scheduled_k?platform=web&store=web&_=1595292439896'
    r = requests.get(link, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup).split(',"data":')[1].split('"id":"home_scheduled_k"}}')[0]+'"id":"home_scheduled_k"}'

    for i in text:
        try:
            if a == 139:
                # print('끝')
                a = 1
                break
            url = 'https://www.lezhin.com'+text.split('"targetUrl":')[a].split('","')[0].split('"')[1].strip()
            title = text.split('","title":"')[a].split('","')[0]
            title_check = titleNull(title)

            a = a+1

            r = requests.get(url, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text2 = str(soup).split('__LZ_PRODUCT__ =')[1].split('__LZ_DATA__ = {')[0].split('all: [{')[1]

            for i in text2:
                try:
                    craw_url = url+'/'+text2.split('"name":"')[b].split('","')[0].strip()
                    title_num = text2.split('"title":"')[b].split('","')[0].strip()
                    if title_num.find('화') != -1:
                        title_num = title_num.split('화')[0].strip()
                    b = b+1

                    data = {
                        'craw_osp_id': 'lezhin',
                        'craw_domain': 'com',
                        'craw_title': title,
                        'craw_site_url' : url,
                        'craw_url': craw_url,
                        'craw_title_num': title_num
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)

                except:
                    b = 1
                    break
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("lezhin 크롤링 시작")
    startCrawling()
    print("lezhin 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
