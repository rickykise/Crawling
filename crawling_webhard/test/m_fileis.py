import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

# pdpop url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = "select cnt_url from cnt_mobile where cnt_osp = 'fileis' and cnt_price = '무료';"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

#DB 업데이트 함수
def dbUpdate(cnt_price,cnt_chk,url):
    sql = "UPDATE cnt_mobile SET cnt_price=%s, cnt_chk=%s  WHERE cnt_url=%s;"
    curs.execute(sql,(cnt_price,cnt_chk,url))
    conn.commit()

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
    }

def startCrawling(url):

    i = 0;a = 1;check = True
    with requests.Session() as s:
        url = url

        post_two  = s.get(url, headers=headers)
        soup = bs(post_two.text, 'html.parser')
        div = soup.find('div', 'vimgbx2')
        if div != None:
            print(url)
            cnt_chk = 0

            cnt_price = div.find_all('span', 'mar_left10')[1].text.replace(",","").split("P")[0].strip()
            if div.find('img', 'mar_left5'):
                img = div.find('img', 'mar_left5')['src']
                if img.find('icon_rp') != -1:
                    cnt_price = div.find('span', 'mar_left5').text.replace(",","").split("P")[0].strip()
                if img.find('icon_affily') != -1:
                    cnt_chk = 1
            if cnt_price.find('이용') != -1:
                cnt_price = cnt_price.split("원")[0].strip()

            print(cnt_price)
            print(cnt_chk)
            print('========================')
            dbUpdate(cnt_price,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',port=3306,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    key = getSearchUrl(conn,curs)

    print("m_fileis 크롤링 시작")
    for s in key:
        startCrawling(s)
    print("m_fileis 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
