import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(url):
    print(url)
    count = 1;cnt_price = 0;returnValue = []
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c.decode('euc-kr','replace'), 'html.parser')
    text = str(soup)

    if text.find("삭제 된") != -1 or text.find("존재하지") != -1:
        sql = "delete from cnt_all where cnt_url=%s;"
        curs.execute(sql,(url))
        conn.commit()
    else:
        ul = str(soup.find('ul', 'dnld_lstcon'))
        li = soup.find('ul', 'dnld_lstcon').find_all('li')
        for item in li:
            if item.find('span', 'packet'):
                cnt_price = item.find('span', 'packet').text.strip().replace(',', '').split("P")[0]
                if cnt_price == '[차단된파일]':
                    count = count+1
                    continue
                cnt_price = int(cnt_price)
            returnValue.append(cnt_price)
        for i in range(len(li)-count):
            cnt_price = returnValue[i]+cnt_price

        print(cnt_price)
        print('===============================================================')

        sql = "UPDATE cnt_all SET cnt_price=%s WHERE cnt_url=%s;"
        curs.execute(sql,(cnt_price,url))
        conn.commit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("pdpop_Price 크롤링 시작")
    for url in getUrl:
        startCrawling(url)
    print("pdpop_Price 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
