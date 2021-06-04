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
    print('검색어 : '+key)
    osp_title = key;idx = keyItem[0]
    link = 'https://www.google.com/search?q='+osp_title+'&tbs=qdr&start=0'
    try:
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('IP address: ') != -1:
            time.sleep(50)
        div = soup.find_all('div', 'kCrYT')

        for item in div:
            if item.find('a'):
                if item.find('span', 'FCUp0c') or item.find('span', 'r0bn4c'):
                    continue
                title = item.find('div', 'BNeawe').text.strip()

                url = item.find('a')['href'].split('url?q=')[1].split('&sa=')[0].replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                url = urllib.parse.unquote(url)
                url = urllib.parse.unquote(url)

                data = {
                    'google_title': title,
                    'google_url' : url,
                    'osp_title': osp_title
                }
                # print(data)
                # print("=================================")

                dbResult = insertGoogle(data)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getGoogleKeyword()

    print("google_webtoon 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("google_webtoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
