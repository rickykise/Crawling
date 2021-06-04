import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def delCheckUp(del_check, url):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'update community_data set del_state=%s where url=%s;'
        curs.execute(sql,(del_check, url))
        conn.commit()
    finally:
        conn.close()

# url 가져오는 함수
def getDelUrl():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT url FROM `union`.community_data where community_name = 'dcinside' and del_state = 0 and textType = '나쁜글' and createDate >= '2020-01-09 00:00:00' order by createDate desc;"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Host': 'gall.dcinside.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# DC삭제글 판단
def startCrawling(url):
    del_check = 0
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    try:
        if text.find('derror/deleted/') != -1:
            del_check = '1'
            dbUpResult = delCheckUp(del_check,url)
    except:
        pass
    # print(url)
    # print(del_check)
    # print("=================================")

if __name__=='__main__':
    start_time = time.time()
    getUrl = getDelUrl()

    print("del_check 크롤링 시작")
    for u in getUrl:
        startCrawling(u)
    print("del_check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
