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

# 제외 검색어 가져오는 함수
def getUrl():
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT host_url FROM sbs.cnt_f_list where cnt_osp = 'newasiantv' and not host_url like '%http%';"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a


def testUp(reNew,url):
    sql = "update cnt_f_list set host_url=%s where host_url=%s;"
    curs.execute(sql,(reNew,url))
    conn.commit()

def startCrawling(url):
    try:
        url = url
        reNew = 'https://vww.newasiantv.tv' + url
        print(url)
        print(reNew)
        testUp(reNew, url)
    except:
        pass



if __name__=='__main__':
    start_time = time.time()
    getU = getUrl()

    print("test 크롤링 시작")
    for u in getU:
        startCrawling(u)
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
