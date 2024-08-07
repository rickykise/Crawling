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
    i = 0;check = True
    link = "https://www.seriesk.co/category/korea-series/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        list = soup.find('div', 'item_1 items')
        div = list.find_all('div', 'item')

        try:
            for item in div:
                title = item.find('h3', 'rd-title').text.strip()
                title_check = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                url = item.find('h3', 'rd-title').find('a')['href']
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div2 = soup.find('div', id='cap1')
                sub = div2.find_all('p', style='text-align: center;')

                for p in sub:
                    if p.find('a'):
                        host_url = p.find('a')['href']
                        title = p.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'seriesk',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("seriesk 크롤링 시작")
    startCrawling()
    print("seriesk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
