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
    link = 'https://jamics.work/웹툰/'
    val = ['월','화','수','목','금','토','일','열흘']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'section-item-wrap')

        try:
            for item in div:
                url = 'https://jamics.work'+item.find('a', id='title')['href']
                title = item.find('a', id='title')['alt']
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                tr = soup.find('table', 'web_list').find_all('tr')

                for item in tr:
                    craw_url = 'https://jamics.work'+item.find('td')['data-role']
                    title_numCh = titleNull(item.find('td', 'content__title').text.strip())
                    title_num = title_numCh.replace(title_check, '').split("화")[0].strip()

                    data = {
                        'craw_osp_id': 'jamics',
                        'craw_domain': 'work',
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

    print("jamics 크롤링 시작")
    startCrawling()
    print("jamics 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
