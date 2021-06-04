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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    link = 'http://www.onlineonlinetv.net/'+site+'/01/'+site+'-korean-online-tv-list.html'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div', 'post-content').find_all('div',class_=False)

    for item in div:
        try:
            url = item.find('a')['href']
            titleSub = item.find('a').text.strip()
            title_check = titleNull(titleSub)
            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find('div', 'blog-posts').find_all('article', 'post')

            for item in div:
                host_url = item.find('h2').find('a')['href']
                title = item.find('h2').find('a').text.strip()
                title_null = titleNull(title)

                # r = requests.get(host_url)
                # c = r.content
                # soup = BeautifulSoup(c,"html.parser")
                # host_cnt = len(soup.find_all('iframe'))

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'onlineonlinetv',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'china',
                    'cnt_writer': ''
                }
                # print(data)

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("onlineonlinetv 크롤링 시작")
    site = ['2019','2018','2017']
    for s in site:
        startCrawling(s)
    print("onlineonlinetv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
