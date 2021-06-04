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
    link = 'https://hdhd13.net/webtoon/continue_list/'
    val = ['1','2','3','4','5','6','7','8']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'list-row')

        try:
            for item in div:
                url = 'https://hdhd13.net'+item.find('a')['href']
                title = item.find('div', 'section-item-inner')['alt'].strip()
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', 'list-container').find_all('a')

                for item in div:
                    check_url = item['href']
                    if check_url.find('webtoon/content') == -1:
                        continue
                    craw_url = 'https://hdhd13.net'+item['href']
                    title_numCh = titleNull(item.find('td', 'content__title')['alt'].strip())
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'hdhd13',
                        'craw_domain': 'net',
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

    print("hdhd13 크롤링 시작")
    startCrawling()
    print("hdhd13 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
