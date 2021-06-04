import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from checkFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

cnt_osp = 'mfile'
checkNum = '2'

def main(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        cnt_chk = 0

        if soup.find('td', 'td_tit').find('img'):
            aaa = soup.find('td', 'td_tit').find('img')['src']
            if aaa.find('icon_alli') != -1:
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
    getUrl = getSearchUrl(cnt_osp,checkNum,conn,curs)
    conn.close()

    print("mfile 체크2 크롤링 시작")
    for u in getUrl:
        main(u)
    print("mfile 체크2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
