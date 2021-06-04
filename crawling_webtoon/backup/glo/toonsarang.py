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
    link = 'https://toonsarang.wtf/웹툰'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'section-item-title')

        try:
            for item in div:
                url = 'https://toonsarang.wtf'+item.find('a')['href']
                title = item.find('a').text.strip()
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'contents-list').find_all('li')

                for item in li:
                    craw_url = 'https://toonsarang.wtf'+item.find('a')['href']
                    title_numCh = titleNull(item.find('div', 'content-title').text.strip())
                    title_num = title_numCh.split(title_check)[1].split('화')[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')

                    data = {
                        'craw_osp_id': 'toonsarang',
                        'craw_domain': 'wtf',
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

    print("toonsarang 크롤링 시작")
    site = ['','/작품/완결']
    for s in site:
        startCrawling(s)
    print("toonsarang 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
