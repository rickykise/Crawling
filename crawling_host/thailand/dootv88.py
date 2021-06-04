import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import ssl
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

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}
    # try:
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    print(soup)
    sub = soup.find('div', 'td-post-content').find_all('p', style='text-align: center;')
    for item in sub:
        if item.find('a'):
            host_url = item.find('a')['href']
            title = item.find('a').text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dootv88',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'thailand',
                'cnt_writer': ''
            }
            print(data)
            print("=================================")

                # dbResult = insertALL(data)
    # except:
    #     pass

    # dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("dootv88 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("dootv88 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
