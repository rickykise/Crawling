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
    link = 'http://safe.ggongt.com/bbs/board.php?bo_table=webtoon'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'list-container').find('ul', 'weeklytype').find_all('li')

        try:
            for item in li:
                div = item.find_all('div', 'toonwrap')
                for item in div:
                    url = 'http://safe.ggongt.com'+item.find('a')['href']
                    title = item.find('div', 'tinfo').find('span').text.strip()
                    title_check = titleNull(title)
                    url = 'http://safe.ggongt.com/bbs/board.php?bo_table=webtoon&wr_id=1'

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    li = soup.find('div', 'serial-list').find_all('li', 'list-item')

                    for item in li:
                        craw_url = 'http://safe.ggongt.com'+item.find('a')['href']
                        span_text = titleNull(item.find('a').find('span').text.strip())
                        title_numCh = titleNull(item.find('a').text.strip())
                        title_num = title_numCh.replace(title_check, '').split('화')[0].strip()
                        if title_num.find(span_text) != -1:
                            title_num = title_num.split('\t')[0].strip()

                        data = {
                            'craw_osp_id': 'safe.ggongt',
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

    print("safe.ggongt 크롤링 시작")
    startCrawling()
    print("safe.ggongt 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
