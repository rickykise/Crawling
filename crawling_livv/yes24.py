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

def startCrawling(item):
    i = 0;check = True;site = item[0];Live_genre = item[1]
    link = 'http://ticket.yes24.com/New/Genre/Ajax/GenreList_Data.aspx?genre='+site+'&sort=3&area=&genretype=1&pCurPage='
    link2 = '&pPageSize=20&_=1611121631820'
    while check:
        i = i+1
        if i == 5:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find_all('a')
        if len(sub) < 2:
            break

        try:
            for item in sub:
                Live_poster = item.find('img')['data-src']
                cnt_num = item['onclick'].split('GoToPerfDetail(')[1].split(')')[0].strip()
                Live_url = 'http://ticket.yes24.com/Perf/'+cnt_num
                Live_kor_title = item['title']
                r = requests.get(Live_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)

                get_text = soup.find('div', 'rn-tab-boxes').find('div', id='rn-tab01')
                Live_txt = str(get_text)

                if text.find('name":["') != -1:
                    Live_search_key = text.split('name":["')[1].split(']')[0].replace('"', '').strip()
                elif text.find('Person","name":"') != -1:
                    Live_search_key = text.split('Person","name":"')[1].split('"')[0].replace('"', '').strip()
                else:
                    Live_search_key = None

                Live_num = 'Live'+datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1000, 9999))
                Live_category = '1'
                Live_state = '2'
                Live_price = text.split('price":"')[1].split('","')[0].strip()
                Live_crawling = 'yes24'
                Live_runtime = text.split('관람시간:')[1].split('분')[0].replace('총', '').replace(' ', '').strip()

                if Live_runtime.find('--') != -1 or Live_runtime.find('-') != -1:
                    Live_runtime = None
                elif Live_runtime.find('시간') != -1:
                    getHour = Live_runtime.split('시간')[0].strip()
                    getHour = int(getHour)*60
                    getMin = Live_runtime.split('시간')[1].strip()
                    getMin = int(getMin)
                    Live_runtime = getHour+getMin
                rating_check = text.split('@context')[1].split('등급:')[1].split('관람시간')[0].strip()
                Live_rating = getRating(rating_check)
                liveCheck = text.split('일시:')[1].split('등급')[0].strip()
                live_start = liveCheck.split('~')[0].strip()
                live_end = liveCheck.split('~')[1].strip()
                Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
                Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

                data = {
                    'Live_num': Live_num,
                    'Live_kor_title': Live_kor_title,
                    'Live_poster': Live_poster,
                    'Live_txt': Live_txt,
                    'Live_search_key': Live_search_key,
                    'Live_genre': Live_genre,
                    'Live_runtime': Live_runtime,
                    'Live_rating': Live_rating,
                    'Live_url': Live_url,
                    'Live_price': Live_price,
                    'Live_category': Live_category,
                    'Live_state' : Live_state,
                    'Live_start_date' : Live_start_date,
                    'Live_end_date' : Live_end_date,
                    'Live_crawling': Live_crawling
                }
                # print(data['Live_rating'])
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("yes24 크롤링 시작")
    site = [['15456', '1'],['15457', '3'],['15458', '4'],['999', '4']]
    for s in site:
        startCrawling(s)
    print("yes24 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
