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
    link = 'https://funbe.icu/웹툰/'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'section-item')

        try:
            for item in div:
                url = 'https://funbe.icu'+item.find('a', id='title')['href']
                title = item.find('a')['alt']
                title_check = titleNull(title)

                # 키워드 체크
                getT = getTitle()
                titleCheck = checkTitle(title_check, getT)
                if titleCheck['m'] == None:
                    continue
                title = titleCheck['m']
                cp_id = titleCheck['i']
                cnt_id = titleCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                tr = soup.find('table', 'web_list').find_all('tr', 'tborder')

                for item in tr:
                    craw_url = 'https://funbe.icu'+item.find('td', 'content__title')['data-role']
                    title_numCh = titleNull(item.find('td', 'content__title')['alt'])
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'funbe',
                        'craw_cp_id' : cp_id,
                        'craw_cnt_id': cnt_id,
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

    print("funbe 크롤링 시작")
    site = ['일','월','화','수','목','금','토','열흘','완결']
    for s in site:
        startCrawling(s)
    print("funbe 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
