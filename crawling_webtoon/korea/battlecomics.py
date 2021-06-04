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
    link = 'http://www.battlecomics.co.kr/webtoons/schedules#week-table'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    sub = soup.find('section', id='week-table').find_all('a', 'webtoon-card')

    for item in sub:
        try:
            url = 'http://www.battlecomics.co.kr'+item['href']
            title = item.find('div', 'webtoon-card__name').text.strip()

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find_all('a', 'episode-list__item')

            for item in sub:
                craw_url = 'http://www.battlecomics.co.kr'+item['href']
                title_num = item.find('h4', 'episode__title').text.split('화')[0].strip()
                if title_num.find('화') != -1:
                    title_num = item.find('h4', 'episode__title').text.split('화')[0].strip()
                elif title_num.find('-') != -1:
                    title_num = item.find('h4', 'episode__title').text.split('-')[0].strip()


                data = {
                    'craw_osp_id': 'battlecomics',
                    'craw_domain': 'co.kr',
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

    print("battlecomics 크롤링 시작")
    startCrawling()
    print("battlecomics 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
