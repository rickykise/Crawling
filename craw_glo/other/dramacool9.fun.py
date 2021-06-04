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
    link = 'https://dramacool9.fun/genre/kshow/page/'
    while check:
        i = i+1
        if i == 10:
            break
        r = requests.get(link+str(i)+'/')
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        article = soup.find_all('article',  id=re.compile("post-+"))

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('img')['alt'].strip()
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
            
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find('ul',  'episodios').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'dramacool9.fun',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dramacool9.fun 크롤링 시작")
    startCrawling()
    print("dramacool9.fun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
