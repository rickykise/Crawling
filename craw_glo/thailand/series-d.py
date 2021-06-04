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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)


def startCrawling():
    i = 0;check = True
    link = 'https://series-d.com/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'series-grid')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('div', 'title-en').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                host_url = url

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'series-d',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'thailand',
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

    print("series-d 크롤링 시작")
    startCrawling()
    print("series-d 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
