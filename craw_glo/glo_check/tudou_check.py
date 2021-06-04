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
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

# cnt_f_list DB 업데이트 함수
def dbUpdate(checkNum,now,host_url):
    if checkNum == 1:
        sql = "update cnt_f_list set cnt_chk=4, cnt_regdate2=%s, cnt_dend_act=1, cnt_dend_date=%s where host_url=%s;"
        curs.execute(sql,(now,now,host_url))
        conn.commit()
    else:
        sql = "update cnt_f_list set cnt_regdate2=%s where host_url=%s;"
        curs.execute(sql,(now,host_url))
        conn.commit()


def startCrawling(url, chekc_item):
    i = 0;check = True;checkNum = 0
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # checkDate = chekc_item[0]
    # limitDate = str(chekc_item[0]  + timedelta(30))
    # if now < limitDate:
    try:
        print(url)
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        if text.find('css/pc/common/404') != -1:
            print('404')
            checkNum = 1
            dbUpdate(checkNum,now,url)
        else:
            print('정상')
            dbUpdate(checkNum,now,url)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getTudouUrl()

    print("youku_list 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("youku_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
