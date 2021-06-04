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
    link = 'https://biluhay.net/quoc-gia/han-quoc/trang-'
    while check:
        i = i+1
        if i == 69:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('ul',  'list-film').find_all('li',  'film-item')

        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
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
                url2 = soup.find('a',  'btn-see')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                episodes = soup.find('div',  'episodes').find_all('ul',  'list-episode')

                for item1 in episodes:
                    li = item1.find_all('li')
                    for item2 in li:
                        host_url = item2.find('a')['href']
                        title = titleSub+'_'+item2.find('a').text.strip()
                        title_null = titleNull(title)
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'biluhay.net',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("biluhay.net 크롤링 시작")
    startCrawling()
    print("biluhay.net 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
