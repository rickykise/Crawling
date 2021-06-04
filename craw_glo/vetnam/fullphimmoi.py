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
    i = 0;check = True
    link = 'https://fullphimmoi.com/quoc-gia/han-quoc/trang-'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('div',  'w-dyn-items').find_all('div', 'w-dyn-item')

        try:
            for item in li:
                url = item.find('a','item-block-title')['href']
                titleSub = item.find('a','item-block-title').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', 'button_xemphim')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                ul = soup.find_all('ul',  'list-episode')

                for item in ul:
                    li = item.find_all('li')
                    for item2 in li:
                        host_url = item2.find('a')['href']
                        titleNum = item2.find('a').text.strip()
                        title = titleSub+'_'+titleNum
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'fullphimmoi',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url': host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("fullphimmoi 크롤링 시작")
    startCrawling()
    print("fullphimmoi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
