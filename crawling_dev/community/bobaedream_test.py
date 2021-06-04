# bobaedream 검색
import sys
import openpyxl,time,pymysql,datetime
import requests
import commonFun
import urllib.request
from commonFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import os, ssl

# headers = {
#     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'ko-KR',
#     'Connection': 'Keep-Alive',
#     'Host': 'www.bobaedream.co.kr',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
#     }

def startCrawling(key):
    print("키워드 : ",key)
    # key = urllib.parse.quote(key)
    pageNum = 1;insertNum = 0;ninsertNum = 0;paramKey = None;check = False
    with requests.Session() as s:
        site = "https://www.bobaedream.co.kr"
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
            ssl._create_default_https_context = ssl._create_unverified_context
        post_one  = s.get(site)
        content = post_one.content
        soup = bs(content.decode('euc-kr','replace'), 'html.parser')
        print(soup)


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("bobaedream 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("bobaedream 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
