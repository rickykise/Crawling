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
    link = 'https://protoon21.com/toon/mais?typ_=normal&cpa_='
    while check:
        i = i+1
        if i == 40:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', 'glis').find_all('a', 'boxs')

        try:
            for item in sub:
                url = 'https://protoon21.com'+item['href']
                title = item.find('div', 'nsti').text.strip()
                title_check = titleNull(title)

                a = 0;pageCheck = True
                page_url = url+'&cps_='
                while pageCheck:
                    a = a+1
                    if a == 10:
                        break
                    r = requests.get(page_url+str(a))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    sub = soup.find('div', 'body').find_all('a')
                    if len(sub) < 1:
                        pageCheck=False;break

                    for item in sub:
                        craw_url = 'https://protoon21.com'+item['href']
                        title_num = item.find('div', 'econ').text.strip()
                        if title_num.find('화') != -1:
                            title_num = title_num.split('화')[0].strip()
                        if url.find('&cp') != -1:
                            url = url.split('&cp')[0].strip()
                        if craw_url.find('&cp') != -1:
                            craw_url = craw_url.split('&cp')[0].strip()

                        data = {
                            'craw_osp_id': 'protoon21',
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

    print("protoon21 크롤링 시작")
    startCrawling()
    print("protoon21 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
