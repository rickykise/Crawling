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
    link = 'http://www.redton32.com'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'item-list').find_all('div', 'item')

        try:
            for item in div:
                url = item.find('a')['href']
                url = 'http://www.redton32.com//list'+url.split('list')[1]
                title = item.find_all('div')[2].text.strip()
                if title == '':
                    title = item.find_all('div')[3].text.strip()
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'detail-items').find('div', 'item-banner').find_all('a')

                for item in sub:
                    craw_url = item['href']
                    if craw_url.find('redton32') == -1:
                        continue
                    title_numCh = titleNull(item.find('span').text.strip())
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'redton32',
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

    print("redton32 크롤링 시작")
    site = ['//wt/0/0/0','//wd/1/0/0']
    for s in site:
        startCrawling(s)
    print("redton32 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
