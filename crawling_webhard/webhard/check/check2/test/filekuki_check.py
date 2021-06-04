import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from checkFun import *

cnt_osp = 'filekuki'
checkNum = '3'

def main(url):
    with requests.Session() as s:
        headers = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')

        try:
            post_one  = s.get(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0

            if soup.find('img', alt='제휴'):
                cnt_chk = 1
        except:
            cnt_chk = 2

    if now >= checkDate:
        sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
        curs.execute(sql,(cnt_chk,url))
        conn.commit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl2(cnt_osp,checkNum,conn,curs)
    conn.close()

    print("filekuki 체크3 크롤링 시작")
    for u in getUrl:
        main(u)
    print("filekuki 체크3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
