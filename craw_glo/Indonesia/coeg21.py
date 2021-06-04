import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
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
    link = 'https://coeg21.net/nonton-drama-korea-sub-indo/'
    r = requests.get(link)
    c = r.text
    soup = BeautifulSoup(c, "html.parser")
    div = soup.find_all('div', 'ml-item')
    for item in div:
        url = item.find('a')['href']
        titleSub = item.find('div','judul').text.strip()
        if titleSub.find('(') != -1:
            titleSub = titleSub.split('(')[0].strip()
        title_check = titleNull(titleSub)
        # 키워드 체크
        getKey = getKeyword()
        keyCheck = checkTitle(title_check,  getKey)
        if keyCheck['m'] == None:
            continue
        cnt_id = keyCheck['i']
        cnt_keyword = keyCheck['k']

        r = requests.get(url)
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        sub = soup.find('div', 'les-content').find_all('a')

        for item in sub:
            host_url = item['href']
            title = titleSub+'_'+item.text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp': 'coeg21',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url': host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'indonesia',
                'cnt_writer': ''
            }
            # print(data)
            # print("=================================")
            
            dbResult = insertALL(data)


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("coeg21 크롤링 시작")
    startCrawling()
    print("coeg21 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
