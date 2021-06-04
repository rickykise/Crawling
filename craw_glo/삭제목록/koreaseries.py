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

def startCrawling():
    i = 0;check = True
    link = 'http://koreaseries.fanthai.com/?cat=2054&paged='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', id='content').find_all('div', 'post')
        try:
            for item in div:
                url = item.find('h2', 'entry-title').find('a')['href']
                titleSub = item.find('h2', 'entry-title').find('a').text.strip()
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', id='content').find_all('div', 'post')

                for item in div:
                    host_url = item.find('h2', 'entry-title').find('a')['href']
                    title = item.find('h2', 'entry-title').find('a').text.strip()
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    host_cnt = len(soup.find('div', 'entry-content').find_all('p', style="text-align: center;"))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'koreaseries',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': host_cnt,
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

    print("koreaseries 크롤링 시작")
    startCrawling()
    print("koreaseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
