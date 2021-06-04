# 인스타그램 크롤링
import datetime, time
import requests
import pymysql
import re
from snsFun import *
from datetime import date, timedelta
from dateutil import tz
from dateutil.parser import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def startCrawling(url, idx):
    # print(url)
    # print(idx[0])
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        data = {
            'like_num' : 0,
            'reply_num' : 0
        }

        metaTag = soup.find(property="og:description")['content']
        if metaTag.find('Likes') != -1:
            data['like_num'] = metaTag.split('Likes')[0].replace(',', '').strip()
            data['reply_num'] = metaTag.split('Likes')[1].split('Comments')[0].replace(',', '').strip()
        else:
            text = str(soup)
            data['like_num'] = text.split('edge_media_preview_like')[1].split('count"')[1].split('"edges')[0].replace(',', '').replace(':', '').strip()
        # print(data)
        # print("=======================")

        dbUpdate = dbUpdateIdx(data['like_num'],data['reply_num'],idx[0])
    except:
        pass




if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = updateIdx(conn,curs)
    conn.close()

    print("인스타그램 크롤링 시작")
    for u, i in dbKey.items():
        startCrawling(u, i)
    print("인스타그램 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
