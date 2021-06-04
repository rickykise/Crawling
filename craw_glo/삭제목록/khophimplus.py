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
    link = 'http://khophimplus.com/country/han-quoc/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(soup)
        li = soup.find('ul', 'halim_box').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                title = item.find('div', 'main-title').text.replace('\n', '').strip()
                if title.find('(') != -1:
                    title = title.split('(')[0]
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                host_url = soup.find('div', 'halim-movie-button').find('a')['href']
                if host_url.find('down') != -1:
                    host_url = soup.find('div', 'halim-movie-button').find_all('a')[1]['href']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'khophimplus',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': 1,
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vietnam',
                    'cnt_writer': ''
                }
                print(data)
                print("=================================")

                # dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("khophimplus 크롤링 시작")
    startCrawling()
    print("khophimplus 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
