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
    link = 'http://8maple.ru/category/分類/韓劇/韓劇2019/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'nag cf').find_all('div', 'item')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
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
                td = soup.find('div', 'rich-content').find('table').find_all('td')

                for item in td:
                    if item.find('a'):
                        if item.find('a')['href'].find('to/') != -1:
                            host_url = item.find('a')['href']
                            title = titleSub + item.find('a').text.strip()
                            title_null = titleNull(title)

                            r = requests.get(host_url)
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")
                            host_cnt = len(soup.find('div', 'videolist').find_all('a'))

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : '8maple',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': host_cnt,
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'china',
                                'cnt_writer': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("8maple 크롤링 시작")
    startCrawling()
    print("8maple 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
