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
    link = 'https://wtwt21.com/'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'gallery').find_all('li')

        try:
            for item in li:
                url = 'https://wtwt21.com'+item.find('a')['href']
                title = item.find('img')['alt']
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'list').find_all('li')

                for item in li:
                    craw_url = 'https://wtwt21.com'+item.find('a')['href']
                    title_numCh = titleNull(item.find('div', 'subject').text.strip())
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()
                    if title_num.find('오늘') != -1:
                        title_num = title_num.split('오늘')[1]
                    elif title_num.find('일전') != -1:
                        title_num = title_num.split('일전')[1]

                    data = {
                        'craw_osp_id': 'wtwt21',
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

    print("wtwt21 크롤링 시작")
    site = ['w1','w2']
    for s in site:
        startCrawling(s)
    print("wtwt21 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
