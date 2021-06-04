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
    link = 'https://comic.naver.com/webtoon/'
    # val = ['weekday.nhn','finish.nhn']
    val = ['weekday.nhn']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'list_area').find_all('li')

        try:
            for item in li:
                url = 'https://comic.naver.com'+item.find('a')['href']
                title = item.find('img')['title']
                title_check = titleNull(title)

                i = 0;check = True
                s_url = url+'&page='
                while check:
                    i = i+1
                    if i == 30:
                        break
                    r = requests.get(s_url+str(i))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    tr = soup.find('table', 'viewList').find_all('tr', class_=None)

                    for item in tr:
                        if item.find('td'):
                            craw_url = 'https://comic.naver.com'+item.find('a')['href']
                            title_num = item.find('img')['title'].split('화')[0].strip()

                            data = {
                                'craw_osp_id': 'naver',
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

    print("naver 크롤링 시작")
    startCrawling()
    print("naver 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
