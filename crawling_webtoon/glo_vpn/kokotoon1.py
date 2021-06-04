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
    i = 0;check = True; a = 0
    for i in range(16):
        link = 'https://kokotoon1.com/toon/all/consonant/'+str(a)
        a = a+1
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', id='comic-completed-all').find_all('li')

        try:
            for item in li:
                url = 'https://kokotoon1.com'+item.find('a')['href']
                title = item.find('div', 'homelist-title').text.strip()
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', id='comic-episode-list').find_all('li')

                for item in li:
                    craw_url = 'https://kokotoon1.com'+item.find('a')['href']
                    title_numCh = titleNull(item.find('div', 'episode-title').text.strip())
                    title_num = title_numCh.split(title_check)[1].split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'kokotoon1',
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

    print("kokotoon1 크롤링 시작")
    startCrawling()
    print("kokotoon1 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
