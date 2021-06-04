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

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['osp_id'],data['osp_url'],data['osp_nat'],data['osp_chk'],data['vpn_state'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'osp_list_check'
        data = {
            'osp_id': args[0],
            'osp_url': args[1],
            'osp_nat': args[2],
            'osp_chk': args[3],
            'vpn_state': args[4],
            'osp_regdate': now
        }

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
        else:
            result = True
            conn.rollback()
    finally:
        return result

# site_url 가져오는 함수
def getChekOspUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    with conn.cursor() as curs:
        sql = "select osp_url, osp_id, osp_nat from osp_list order by n_idx asc;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
                returnValue[key].append(result[i][2])
            else:
                returnValue.update({key:[result[i][1],result[i][2]]})
        # print(returnValue)

        return returnValue

def startCrawling():
    i = 0;check = True;returnValue = []
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUrl = getChekOspUrl()
    for url, chekc_item in getUrl.items():
        osp_id = chekc_item[0]
        osp_nat = chekc_item[1]
        osp_chk = 1
        try:
            r = requests.get(url, timeout = 2)
            urlState = r.status_code
            if urlState != 200 and urlState != 520 and urlState != 503:
                urlStateRe = siteCheck(osp_id, url)
                if urlStateRe != 200:
                    osp_chk = '0'
                else:
                    osp_chk = '1'

            data = {
                'osp_id': osp_id,
                'osp_url' : url,
                'osp_nat': osp_nat,
                'osp_chk': osp_chk,
                'vpn_state' : '0'
            }
            # print(data)
            # print(urlState)
            # print("=================================")

            dbResult = insertALL(data)
        except:
            pass

if __name__=='__main__':
    start_time = time.time()
    print("osp_insert 재검수 시작")
    startCrawling()
    print("osp_insert 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
