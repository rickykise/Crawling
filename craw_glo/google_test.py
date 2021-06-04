import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
import pymysql,time,datetime

def startCrawling(key):
    print('키워드: '+key)
    i = 0;check = True; cnt_id = 'sbs-sbscp-11932'
    link = 'https://www.google.com/search?q='+key+'&tbs=qdr%3Am&start='
    # try:
    while check:
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'kCrYT')

        for item in div:
            if item.find('a'):
                title = item.find('div', 'BNeawe').text.strip()
                title_null = titleNull(title)
                # googleCheck = googleCheckTitle(title_null, key, cnt_id)
                # if googleCheck == None:
                #     continue
                url = item.find('a')['href'].split('url?q=')[1].split('&sa=')[0].replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                # url 체크
                urlGet = getUrl()
                urlCheck = checkUrl(url, urlGet)
                if urlCheck['m'] != None:
                    continue

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'google',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': 'cnt_keyword',
                    'cnt_nat': 'unitedstates',
                    'cnt_writer': '',
                    'origin_url': '',
                    'origin_osp': '',
                    'cnt_keyword_nat': 'en'
                }
                print(data)
                print("=================================")

                # dbResult = insertALLKey(data)
        i = i+10
        if i == 100:
            check=False;break
    # except:
    #     pass

if __name__=='__main__':
    start_time = time.time()

    print("google 크롤링 시작")
    key = ['Vương Hậu Cuối Cùng', 'An Empress’s Dignity']
    for k in key:
        startCrawling(k)
    print("google 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
