import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup

def gloDelUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    with conn.cursor() as curs:
        sql = "select osp_url, osp_id from osp_list where osp_state = 0 and osp_del = 0;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})

        return returnValue

# cnt_f_list DB 업데이트 함수
def dbUpdate(checkNum, url):
    if checkNum == 1:
        sql = "update osp_list set osp_del='1' where osp_url=%s;"
        curs.execute(sql,(url))
        conn.commit()
    else:
        sql = "update osp_list set osp_state='1' where osp_url=%s;"
        curs.execute(sql,(url))
        conn.commit()

def startCrawling(url, id):
    chUrl="";reUrl="";checkNum="0"
    try:
        r = requests.get(url)
        urlState = r.status_code
        if urlState == 200:
            chUrl = r.url
            if chUrl.find('http://') != -1:
                chUrl = chUrl.split('http://')[1].replace('/', '').strip()
            elif chUrl.find('https://') != -1:
                chUrl = chUrl.split('https://')[1].replace('/', '').strip()
            if url.find('http://') != -1:
                reUrl = url.split('http://')[1].replace('/', '').strip()
            elif url.find('https://') != -1:
                reUrl = url.split('https://')[1].replace('/', '').strip()

            if reUrl == chUrl:
                dbUpdate(checkNum,url)
            else:
                checkNum = '1'
                dbUpdate(checkNum,url)
        else:
            checkNum = '1'
            dbUpdate(checkNum,url)
    except:
        checkNum = '1'
        dbUpdate(checkNum,url)
        pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = gloDelUrl()

    print("osp delcheck 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("osp delcheck 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
