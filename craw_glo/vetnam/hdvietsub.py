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
    link = 'https://hdvietsub.net/quoc-gia/han-quoc/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find_all('li',  'TPostMv')

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
                url2 = soup.find('div',  'Image').find('a')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find_all('ul',  'list-episode')[1].find_all('li',  'episode')

                for item in li:
                    host_url = item.find('a')['href']
                    titleNum = item.find('a').text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'hdvietsub',
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

    print("hdvietsub 크롤링 시작")
    startCrawling()
    print("hdvietsub 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
