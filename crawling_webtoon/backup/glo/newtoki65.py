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

def startCrawling(site):
    i = 0;check = True
    link = 'https://newtoki65.com/webtoon/p'
    link2 = '?toon='+site
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', id='webtoon-list-all').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                title = item['date-title']
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'list-body').find_all('li')

                for item in li:
                    craw_url = item.find('a')['href']
                    if craw_url.find('&spage') != -1:
                        craw_url = craw_url.split('&spage')[0]
                    craw_url = urllib.parse.unquote(craw_url)
                    title_numCh = titleNull(item.find('a').text.strip())
                    title_num = title_numCh.split(title_check)[1].split("화")[0].strip()
                    if title_num.find('제') != -1:
                        title_num = title_num.split('제')[1].strip()

                    data = {
                        'craw_osp_id': 'newtoki65',
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

    print("newtoki65 크롤링 시작")
    site = ['일반웹툰','성인웹툰','BL%2FGL','완결웹툰']
    for s in site:
        startCrawling(s)
    print("newtoki65 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
