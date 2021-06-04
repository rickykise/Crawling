import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import dailymotion
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    # recent relevance
    link = 'https://api.dailymotion.com/videos/?search='+key+'&sort=recent&page=1&limit=100'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)

    try:
        for item in text:
            cnt_num = text.split('"id":"')[a].split('",')[0]
            a = a+1
            if a == 101:
                a = 1
                break
            url = 'https://www.dailymotion.com/video/'+cnt_num
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")

            title = soup.find('title').text.strip()
            if title.find('- video') != -1:
                title = title.split('- video')[0].strip()
            title = setText(title, 0)
            title_null = titleNull(title)
            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_null, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dailymotion',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'france',
                'cnt_writer': '',
                'origin_url': '',
                'origin_osp': '',
                'cnt_keyword_nat': k_nat
            }
            # print(data)
            # print("=================================")

            dbResult = insertALLKey(data)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeywordDaily()

    print("dailymotion 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("dailymotion 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
