import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import random
from livvFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = 'https://ticket.melon.com/performance/ajax/prodList.json?commCode=&sortType=REAL_RANK&perfGenreCode='+site+'_ALL&perfThemeCode=&filterCode=FILTER_ALL&v=1'
    while check:
        i = i+1
        if i == 2:
            break
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Host': 'ticket.melon.com',
            'Referer': 'https://ticket.melon.com/concert/index.htm?genreType='+site,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest'
        }

        a = 1
        r = requests.get(link, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                Live_num = 'Live'+datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1000, 9999))
                Live_poster = 'https://cdnticket.melon.co.kr'+text.split('posterImg":"')[a].split('","')[0].strip()
                Live_kor_title = text.split('"title":"')[a].split('","')[0].strip()
                checkGenre = text.split('perfTypeName":"')[a].split('","')[0].strip()
                if checkGenre == '콘서트':
                    Live_genre = 1
                elif checkGenre == '뮤지컬':
                    Live_genre = 3
                else:
                    Live_genre = 4
                if Live_kor_title.find('팬미팅') != -1:
                    Live_genre = 2
                Live_price = text.split('basePrice')[a].split(',')[0].strip()
                Live_price = Live_price.split(':')[1].strip()
                Live_crawling = 'melon'
                Live_runtime = text.split('runningTime":"')[a].split('","')[0].replace('분', '').strip()
                if Live_runtime == '-':
                    Live_runtime = None
                if Live_runtime.find('(') != -1:
                    Live_runtime = Live_runtime.split('(')[0].strip()
                cnt_num = text.split('prodId":')[a].split(',"')[0].strip()
                Live_url = 'https://ticket.melon.com/performance/index.htm?prodId='+cnt_num
                Live_category = '1'
                Live_state = '2'
                a = a+1

                r = requests.get(Live_url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                if soup.find('ul', 'list_artist'):
                    li = soup.find('ul', 'list_artist').find_all('li')
                    lst=[]
                    for item in li:
                        search_key = item.find('a', 'txt_name').find('strong').text.strip()
                        lst.append(search_key)
                    Live_search_key = ",".join(lst)

                    data = {
                        'Live_num': Live_num,
                        'Live_kor_title': Live_kor_title,
                        'Live_poster': Live_poster,
                        'Live_search_key': Live_search_key,
                        'Live_genre': Live_genre,
                        'Live_runtime': Live_runtime,
                        'Live_url': Live_url,
                        'Live_price': Live_price,
                        'Live_category': Live_category,
                        'Live_state' : Live_state,
                        'Live_crawling': Live_crawling
                    }

                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
                else:
                    Live_search_key = None

                    data = {
                        'Live_num': Live_num,
                        'Live_kor_title': Live_kor_title,
                        'Live_poster': Live_poster,
                        'Live_search_key': Live_search_key,
                        'Live_genre': Live_genre,
                        'Live_runtime': Live_runtime,
                        'Live_url': Live_url,
                        'Live_price': Live_price,
                        'Live_category': Live_category,
                        'Live_state' : Live_state,
                        'Live_crawling': Live_crawling
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            a = 1
            break

if __name__=='__main__':
    start_time = time.time()

    print("interpark 크롤링 시작")
    site = ['GENRE_CON', 'GENRE_ART']
    for s in site:
        startCrawling(s)
    print("interpark 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
