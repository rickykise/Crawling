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
    i = 0;check = True
    link = 'http://dramaqu.net/drama-list/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'film-content category').find_all('div', 'list_items')

        try:
            for item in div:
                cnt_url = item.find('span', 'movie-title').find('a')['href']
                title = item.find('span', 'movie-title').find('a').text.strip()
                if title.find('(') != -1:
                    title = title.split('(')[0].strip()
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                    
                r = requests.get(cnt_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                cnt_num = soup.find('div', 'stars')['data-id']

                data = {
                    'cnt_num' : cnt_num,
                    'cnt_osp' : 'dramaqu',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'cnt_url' : cnt_url,
                    'cnt_host' : '',
                    'cnt_writer' : '',
                    'cnt_nat': 'indonesia'
                }
                # print(data)

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("dramaqu 크롤링 시작")
    startCrawling()
    print("dramaqu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
