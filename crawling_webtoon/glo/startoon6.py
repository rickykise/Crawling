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

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'}

def startCrawling(site):
    i = 0;check = True
    link = 'https://startoon6.com/bbs/board.php?bo_table=webtoon'+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list column-8').find_all('li')

        try:
            for item in li:
                url = 'https://startoon6.com/bbs'+item.find('a')['href'].split('/bbs')[1].split('&page')[0].strip()
                title = item.find('h3', 'item-title').text.strip()
                title_check = titleNull(title)

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                tr = soup.find('table', id='series').find('tbody').find_all('tr')

                for item in tr:
                    craw_url = 'https://startoon6.com/bbs'+item['onclick'].split('/bbs')[1].split("'")[0].strip()
                    title_numCh = titleNull(item.find('td').text.strip())
                    title_num = title_numCh.replace(title_check, '').split("회")[0].strip()

                    data = {
                        'craw_osp_id': 'startoon6',
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

    print("startoon6 크롤링 시작")
    site = ['1','2','3']
    for s in site:
        startCrawling(s)
    print("startoon6 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
