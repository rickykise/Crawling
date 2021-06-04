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
    link = 'https://www.toomics.com/webtoon/'
    val = ['toon_list/display/G2','weekly/dow/1','weekly/dow/2','weekly/dow/3','weekly/dow/4','weekly/dow/5','weekly/dow/6','weekly/dow/7']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', id='more_list').find_all('li')

        try:
            for item in li:
                url = 'https://www.toomics.com'+item.find('a')['href']
                if url.find('bridge/type/2') != -1:
                    url = 'https://www.toomics.com'+item.find('a')['href'].replace('bridge/type/2', 'episode')
                title = item.find('div', 'toon-dcard__title-group').text.replace('\n', '').strip()

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'eps epsMoreList').find_all('li')

                for item in li:
                    craw_url = 'https://www.toomics.com'+item.find('a')['href']
                    if craw_url.find('comjavascript') != -1:
                        continue
                    title_num = item.find('div', 'ep__episode').text.strip()

                    data = {
                        'craw_osp_id': 'toomics',
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
            continue

if __name__=='__main__':
    start_time = time.time()

    print("toomics 크롤링 시작")
    startCrawling()
    print("toptoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
