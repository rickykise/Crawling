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

def getKeyword():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT k_title FROM ex_key;"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a

# 검색어 체크키워드 가져오는 함수
def searchId(key):
    key = key.replace(' ', '')
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "select k_cnt_id from sbs.k_word where replace(k_title, ' ', '') like '%"+key+"%';"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a

def searchKey(k_cnt_id):
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "select k_title, k_nat from sbs.k_word where k_cnt_id = %s and k_nat in ('cn','us');"
            curs.execute(sql,(k_cnt_id))
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                else:
                    returnValue.update({key:[result[i][1]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

def insertALL(k, n):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,k,n)
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
        tableName = 'ex_key'
        data = {
            'k_title': args[0],
            'k_nat': args[1]
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


def startCrawling(key):
    print(key)
    k_cnt_id = searchId(key)
    # print(k_cnt_id[0])
    search_key = searchKey(k_cnt_id[0])
    for k, n in search_key.items():
        dbResult = insertALL(k, n[0])
    print("=================================")

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("ex_del 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("ex_del 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
