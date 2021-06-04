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
    link = 'https://www.allall16.net/'+site+'?&page='
    while check:
        i = i+1
        if i == 50:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list-type1').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                title = item.find('img')['alt']
                title_check = titleNull(title)

                a = 0;pageCheck = True
                page_url = url+'/page/'
                while pageCheck:
                    a = a+1
                    if a == 50:
                        break
                    r = requests.get(page_url+str(a))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    li = soup.find('ul', 'episode-list').find_all('li', 'is-purchasable')
                    if len(li) < 2:
                        pageCheck=False;break

                    for item in li:
                        craw_url = item.find('a')['href']
                        title_numCh = titleNull(item.find('div', 'episode-title').text.strip())
                        title_num = title_numCh.split(title_check)[1].split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'allall16',
                            'craw_domain': 'net',
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

    print("allall16 크롤링 시작")
    site = ['publish/index/10','completion/index/1']
    for s in site:
        startCrawling(s)
    print("allall16 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
