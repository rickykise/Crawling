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

def startCrawling(key, keyItem):
    # plusKey = [' 다시보기', ' 다운로드']
    # for k in plusKey:
        # keyword = key+k
    keyword = key+' 다시보기';cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://www.google.com/search?q='+keyword+'&tbs=qdr:d&start='
    while check:
        try:
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find_all('div', 'kCrYT')

            for item in div:
                if item.find('a'):
                    if item.find('span', 'FCUp0c') or item.find('span', 'r0bn4c'):
                        continue
                    title = item.find('div', 'BNeawe').text.strip()
                    googleCheck = googleCheckTitle(title, key, cnt_id)
                    if googleCheck == None:
                        continue
                    title_null = titleNull(title)
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
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'unitedstates',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': '',
                        'cnt_keyword_nat': k_nat
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALLKey(data)
        except:
            continue

        i = i+10
        if i == 100:
            check=False;break

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeywordGoogle()

    print("google 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("google 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
