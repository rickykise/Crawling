import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    a = 1
    link = 'https://www.bomtoon.com/weekly/list/'
    val = ['mon','tue','wed','thu','fri','sat','sun','10']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup).replace('\\', '')

        for i in text:
            try:
                url = 'https://www.bomtoon.com'+text.split('href='+"'"+'"')[a].split('"')[0].strip()
                a = a+1

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                title = soup.find('p', id='bt-comic-name').text.strip()
                li = soup.find('ul', id='bt-episode-list').find_all('li')

                for item in li:
                    craw_url = url.replace('ep_list', 'ep_view')+'/'+item['data-episode-id']
                    title_num = item.find('p', 'ttl').text.split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'bomtoon',
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
                a = 1
                break

if __name__=='__main__':
    start_time = time.time()

    print("bomtoon 크롤링 시작")
    startCrawling()
    print("bomtoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
