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
    link = 'https://phimhaymoingay.net/category/phimhaymoingay.html?sapxep=moicapnhat&form_id=-1&category_id=-1&country_id=3&year_id=-1&page='
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div',  'film-bot').find_all('div',  'film-li')

        try:
            for item in div:
                url = item.find('a')['href']
                title = item.find('div','film-department').text.strip()
                if title.find('(') != -1:
                    title = title.split('(')[0].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', id='btn-film-watch')['href']

                r = requests.get(url2)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                sub = soup.find('div',  'view-sv').find_all('a')

                for item in sub:
                    host_url = item['href']
                    titleSub = item['data-id']
                    title_null = titleNull(titleSub)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'phimhaymoingay',
                        'cnt_title': title+'_'+titleSub,
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

    print("phimhaymoingay 크롤링 시작")
    startCrawling()
    print("phimhaymoingay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
