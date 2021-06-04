import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
import smtplib
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from check_api import *
from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

# db 업데이트
def dbCheckUpdate(osp_chk,n_idx):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update osp_list_check set osp_chk_vpn=%s where n_idx=%s;"
    curs.execute(sql,(osp_chk,n_idx))
    conn.commit()

# site_url 가져오는 함수
def getChekOspUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    with conn.cursor() as curs:
        sql = "select osp_url, n_idx  from osp_list_check where osp_regdate >= curdate() order by n_idx asc;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})
        # print(returnValue)

        return returnValue

def startCrawling():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUrl = getChekOspUrl()
    for url, chekc_item in getUrl.items():
        n_idx = chekc_item[0]
        osp_chk = '1'
        try:
            r = requests.get(url, timeout = 2)
            urlState = r.status_code
            if urlState != 200 and urlState != 520 and urlState != 503:
                urlStateRe = siteCheck(osp_id, url)
                if urlStateRe != 200:
                    osp_chk = '0'
                else:
                    osp_chk = '1'

            # dbResult = dbCheckUpdate(osp_chk, n_idx)
        except:
            osp_chk = '0'
            dbResult = dbCheckUpdate(osp_chk, n_idx)
            pass

if __name__=='__main__':
    start_time = time.time()
    print("osp_list 재검수 시작")
    startCrawling()
    print("osp_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
