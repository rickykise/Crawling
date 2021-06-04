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
    link = 'http://www.ticketlink.co.kr/concert/getConcertList?page='
    link2 = '&categoryId='+site+'&frontExposureYn=Y&productLocationCode='
    while check:
        i = i+1
        if i == 5:
            break
        a = 1
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)

        try:
            for item in text:
                Live_num = 'Live'+datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1000, 9999))
                Live_kor_title = text.split('productName":"')[a].split('","')[0].strip()
                Live_poster = 'https:'+text.split('"productImagePath":"')[a].split('","')[0].strip()

                cnt_num = text.split('productId":')[a].split(',"')[0].strip()
                Live_url = 'http://www.ticketlink.co.kr/product/'+cnt_num
                Live_crawling = 'ticketlink'

                r = requests.get(Live_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text2 = str(soup)

                if text2.find('관람시간') == -1:
                    a = a+1
                    continue

                get_text = soup.find('div', id='tabs-1')
                Live_txt = str(get_text)

                Live_runtime = text2.split('관람시간')[1].split('분')[0].strip()
                Live_runtime = Live_runtime.split('txt">')[1].strip()
                Live_price = text2.split('evt_data.price')[1].split('";')[0].strip()
                Live_price = Live_price.split('"')[1].strip()
                if text2.find('주연</th>') != -1:
                    Live_search_key = text2.split('주연</th>')[1].split('공연장소')[0].strip()
                    Live_search_key = Live_search_key.split('<td>')[1].split('</td>')[0].replace('"', '').strip()
                else:
                    Live_search_key = text2.split('출연자</th>')[1].split('공연장소')[0].strip()
                    Live_search_key = Live_search_key.split('<td>')[1].split('</td>')[0].replace('"', '').strip()
                if Live_search_key == '':
                    Live_search_key = None
                elif Live_search_key.find('참고') != -1:
                    Live_search_key = None
                Live_category = '1'
                Live_state = '2'
                rating_check = soup.find('div', 'etc_info').find('div', 'bx_dummy border_type').find('span', 'txt').text.strip()
                Live_rating = getRating(rating_check)
                liveCheck = text2.split('기간')[1].split('txt">')[1].split('</span>')[0].strip()
                live_start = liveCheck.split('~')[0].strip()
                live_end = liveCheck.split('~')[1].strip()
                Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
                Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

                a = a+1

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
            a = 1
            pass

if __name__=='__main__':
    start_time = time.time()

    print("ticketlink 크롤링 시작")
    site = [['14', '1'],['16', '3'],['15', '4']]
    for s in site:
        startCrawling(s)
    print("ticketlink 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
