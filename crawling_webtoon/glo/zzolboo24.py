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
    link = 'https://zzolboo24.com/toon/continue/week/'
    val = ['1','2','3','4','5','6','7','8','9']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'list-gel-item').find_all('div', id=re.compile("div+"))

        try:
            for item in div:
                url = item.find('a', 'bo_tit')['href']
                title = item.find('a', 'bo_tit').text.strip()
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'card-body')

                for item in div:
                    if len(item) >= 4:
                        continue
                    craw_url = item.find('a')['href']
                    span_text = titleNull(item.find('p').find('span').text.strip())
                    title_numCh = titleNull(item.find('p').text.strip())
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()
                    if title_num.find(span_text) != -1:
                        title_num = title_num.split('\t')[0].strip()

                    data = {
                        'craw_osp_id': 'zzolboo24',
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

    print("zzolboo24 크롤링 시작")
    startCrawling()
    print("zzolboo24 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
