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
    link = "http://ticket.interpark.com/TPGoodsList.asp?Ca="+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('div', 'stit').find('tbody').find_all('tr')

        try:
            for item in tr:
                Live_poster = item.find('img')['src']
                cnt_num = item.find('span', 'fw_bold').find('a')['href'].split('GroupCode=')[1].strip()
                Live_url = 'https://tickets.interpark.com/goods/'+cnt_num
                title = item.find('span', 'fw_bold').find('a').text.strip()
                api_url = 'https://api-ticketfront.interpark.com/v1/goods/'+cnt_num+'/summary?goodsCode='+cnt_num+'&priceGrade=&seatGrade='
                casting_url = 'https://api-ticketfront.interpark.com/v1/goods/'+cnt_num+'/tab/info?goodsCode='+cnt_num+'&kindOfGoods=01011'

                b = 1
                r = requests.get(casting_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)

                lst=[]
                try:
                    for item in text:
                        search_key = text.split('manName":"')[b].split('","')[0].strip()
                        b = b+1
                        lst.append(search_key)
                except:
                    b = 1
                    pass
                Live_search_key = ",".join(lst)

                a = 0
                r = requests.get(api_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)

                for item in text:
                    if a == 1:
                        break
                    Live_num = 'Live'+datetime.datetime.now().strftime('%Y%m%d')+str(random.randint(1000, 9999))
                    Live_kor_title = text.split('goodsName":"')[1].split('","')[0].strip()
                    Live_category = '1'
                    Live_state = '2'
                    Live_price = text.split('minSalesPrice":')[1].split(',"')[0].strip()
                    Live_crawling = 'interpark'
                    Live_runtime = text.split('runningTime":"')[1].split('","')[0].strip()
                    if Live_runtime == '':
                        Live_runtime = None

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
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
                    a = a+1
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("interpark 크롤링 시작")
    site = [['Mus', '3'],['Liv', '1'],['Dra', '4'],['Fam', '4']]
    for s in site:
        startCrawling(s)
    print("interpark 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
