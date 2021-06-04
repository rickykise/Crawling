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

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.tv99.tv/category/'+site
    link2 = '/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+link2+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile("post-+"))


        try:
            for item in article:
                url = item.find('h2', 'entry-title').find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('h2', 'entry-title').find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'tv99',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'taiwan',
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

    print("tv99 크롤링 시작")
    site=['韓綜線上看', 'koreandramaonline']
    for s in site:
        startCrawling(s)
    print("tv99 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
