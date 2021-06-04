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

def startCrawling(key, keyItem):
    i = 0;check = True;keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];
    link = 'http://mfilm.vn/Home/filter?keyword='+keyword
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'content-film-item')

        try:
            for item in div:
                host_url = 'http://mfilm.vn'+item.find('a')['href']
                title = item.find('a').find('img')['alt']+item.find('h3').find('small').text.strip()
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
                    'cnt_osp' : 'mfilm',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': host_url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vietnam',
                    'cnt_writer': '',
                    'origin_url': '',
                    'origin_osp': '',
                    'cnt_keyword_nat': k_nat
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getKey = getKeywordCH()

    print("mfilm 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("mfilm 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
