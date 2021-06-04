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
    link = 'https://www.9tata.com/file/'+site
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            r = requests.get(link+link2)
        else:
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        article = soup.find_all('article',  'u-movie')

        try:
            for item in article:
                url = 'https://www.9tata.com'+item.find('a')['href']
                titleSub = item.find('a').find('h2').text.strip()
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
                li = soup.find('div',  'playbox').find_all('li')

                for item in li:
                    if item.find('a', href=lambda x: x and ".html" in x) == None:
                        continue
                    host_url = 'https://www.9tata.com'+item.find('a', href=lambda x: x and ".html" in x)['href']
                    title = titleSub + '_' + item.find('a', href=lambda x: x and ".html" in x).text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id, 
                        'cnt_osp': '9tata', 
                        'cnt_title': title, 
                        'cnt_title_null': title_null, 
                        'host_url': host_url, 
                        'host_cnt': '1', 
                        'site_url': url, 
                        'cnt_cp_id': 'sbscp', 
                        'cnt_keyword': cnt_keyword, 
                        'cnt_nat': 'china', 
                        'cnt_writer': '',
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

    print("9tata 크롤링 시작")
    site = ['list50_', 'list58_']
    for s in site:
        startCrawling(s)
    print("9tata 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
