import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;check = True
    link = "https://www.serieshot.co/category/korea-series/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        list = soup.find('div', 'item_1 items')
        div = list.find_all('div', 'item')

        try:
            for item in div:
                title = item.find('h2').text.strip()
                title_check = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                k_word = keyCheck['m']
                url = item.find('a')['href']
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div2 = soup.find('div', id='cap1')
                sub = div2.find_all('p', style='text-align: center;')

                for p in sub:
                    if p.find('a'):
                        url = p.find('a')['href']
                        cnt_num = url.split('p/')[1].split('/')[0]
                        title = p.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'glo_num' : cnt_num,
                            'glo_site' : 'serieshot',
                            'glo_nation': 'thailand',
                            'glo_cp': 'SBS',
                            'glo_k_word': k_word,
                            'glo_title': title,
                            'glo_title_null' : title_null,
                            'glo_url' : url
                        }
                        # print(data)

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("serieshot 크롤링 시작")
    startCrawling()
    print("serieshot 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
