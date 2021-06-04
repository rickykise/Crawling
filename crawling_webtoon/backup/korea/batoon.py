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
    if site == "1":
        link = 'http://www.batoon.xyz/bbs/board.php?bo_table=toon_c&sca=001&week='
        val = ['1','2','3','4','5','6','7','8']
        for v in val:
            r = requests.get(link+v)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find('div', 'content-list').find_all('a')

            try:
                for item in sub:
                    url = 'http://www.batoon.xyz'+item['href']
                    title = item.find('h5').text.strip()
                    title_check = titleNull(title)

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    li = soup.find('ul', id='comic-episode-list').find_all('li')

                    for item in li:
                        craw_url = 'http://www.batoon.xyz'+item.find('button')['onclick'].split("href='")[1].split("'")[0].strip()
                        title_numCh = titleNull(item.find('div', 'episode-title').text.strip())
                        title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'batoon',
                            'craw_domain': 'xyz',
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
    else:
        link = 'http://www.batoon.xyz/bbs/board.php?bo_table=toon_c&sca=002&value='
        val = ['ga', 'na', 'da', 'la', 'ma', 'ba', 'sa', 'aa', 'ja', 'ca', 'ka', 'ta', 'pa', 'ha', 'en', 'nu']
        for v in val:
            r = requests.get(link+v)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find('div', 'content-list').find_all('a')

            try:
                for item in sub:
                    url = 'http://www.batoon.xyz'+item['href']
                    title = item.find('h5').text.strip()
                    title_check = titleNull(title)

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    li = soup.find('ul', id='comic-episode-list').find_all('li')

                    for item in li:
                        craw_url = 'http://www.batoon.xyz'+item.find('button')['onclick'].split("href='")[1].split("'")[0].strip()
                        title_numCh = titleNull(item.find('div', 'episode-title').text.strip())
                        title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'batoon',
                            'craw_domain': 'xyz',
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

    print("batoon 크롤링 시작")
    site = ['1','2']
    for s in site:
        startCrawling(s)
    print("batoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
