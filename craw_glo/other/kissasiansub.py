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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    check = True
    r = requests.get('https://kissasiansub.me/author/kissasian/')
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    i = int(soup.find('span', 'pages').text.split('of')[1].strip())

    link = "https://kissasiansub.me/author/kissasian/page/"
    while check:
        if i == 0:
            break
        r = requests.get(link+str(i))
        i = i-1
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'item-list')

        try:
            for item in article:
                host_url = item.find('a')['href']
                title = item.find('a').text.strip()
                if title.find('Hello world') != -1:
                    continue
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'kissasiansub',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': host_url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'other',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kissasiansub 크롤링 시작")
    startCrawling()
    print("kissasiansub 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
