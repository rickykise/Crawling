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

def startCrawling(key, keyItem):
    Live_url = key; cnt_id = keyItem[0]
    print(Live_url)
    print(cnt_id)
    print("=================================")

    if cnt_id == "interpark":
        try:
            cnt_num = Live_url.split('goods/')[1]
            api_url = 'https://api-ticketfront.interpark.com/v1/goods/'+cnt_num+'/summary?goodsCode='+cnt_num+'&priceGrade=&seatGrade='

            r = requests.get(Live_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            liveCheck = text.split('일시:')[1].split('등급')[0].strip()
            live_start = liveCheck.split('~')[0].strip()
            live_end = liveCheck.split('~')[1].strip()
            Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
            Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

            dbResult = dbUpdate(Live_start_date, Live_end_date, Live_url)

        except:
            continue
    elif cnt_id == 'melon':
        try:
            r = requests.get(Live_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            liveCheck = text.split('일시:')[1].split('등급')[0].strip()
            live_start = liveCheck.split('~')[0].strip()
            live_end = liveCheck.split('~')[1].strip()
            Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
            Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

            dbResult = dbUpdate(Live_start_date, Live_end_date, Live_url)

        except:
            continue
    elif cnt_id == 'ticketlink':
        try:
            r = requests.get(Live_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            liveCheck = text.split('일시:')[1].split('등급')[0].strip()
            live_start = liveCheck.split('~')[0].strip()
            live_end = liveCheck.split('~')[1].strip()
            Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
            Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

            dbResult = dbUpdate(Live_start_date, Live_end_date, Live_url)

        except:
            continue
    elif cnt_id == 'yes24':
        try:
            r = requests.get(Live_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            liveCheck = text.split('일시:')[1].split('등급')[0].strip()
            live_start = liveCheck.split('~')[0].strip()
            live_end = liveCheck.split('~')[1].strip()
            Live_start_date = datetime.datetime.strptime(live_start, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')
            Live_end_date = datetime.datetime.strptime(live_end, '%Y.%m.%d').strftime('%Y-%m-%d %H:%M:%S')

            dbResult = dbUpdate(Live_start_date, Live_end_date, Live_url)

        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    getL = getLive()

    print("update 크롤링 시작")
    for u, i in getL.items():
        startCrawling(u, i)
    print("update 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
