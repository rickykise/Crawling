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

def startCrawling(site):
    i = 0;check = True
    link = 'http://173.233.87.137/kategori/'+site+'/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div', 'content').find_all('div', 'post-boxed')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('span').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                url2 = url+'#episode'

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                div = soup.find('div', 'masonry').find_all('div','post-boxed')

                for item in div:
                    host_url = item.find('a')['href']
                    title = item.find('img')['alt'].strip()
                    if title.find('Trailer') != -1:
                        continue
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'drakor',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("drakor 크롤링 시작")
    site = ['drama-korea', 'variety-show']
    for s in site:
        startCrawling(s)
    print("drakor 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
