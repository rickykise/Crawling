import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
from requests import Session
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    link = 'https://www.inw-series.com/category/%e0%b8%8b%e0%b8%b5%e0%b8%a3%e0%b8%b5%e0%b9%88%e0%b8%a2%e0%b9%8c%e0%b9%80%e0%b8%81%e0%b8%b2%e0%b8%ab%e0%b8%a5%e0%b8%b5/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    article = soup.find_all('article',  id=re.compile('post-+'))

    for item in article:
        try:
            url = item.find('a')['href']
            url = urllib.parse.unquote(url)
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
            playlist = soup.find('article',  id=re.compile('post-+')).find('div', "entry-content").find_all('p',style=lambda value: value and 'text-align: center;' in value)

            for item in playlist:
                host_url = item.find('a')['href']
                title = item.find('a').text.strip()
                title_null = titleNull(title)


                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp': 'inw-series',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url': host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'thailand',
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

    print("inw-series 크롤링 시작")
    startCrawling()
    print("inw-series 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
