import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
# from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

#insertall
def insertALLDB(data):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['osp_id'],data['osp_url'],data['osp_nat'],data['osp_chk'],data['vpn_state'],data['osp_regdate'])
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
            'osp_regdate': args[5]
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

# backupDB 가져오는 함수
def getListDB():
    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    result = None
    with conn.cursor() as curs:
        try:
            sql = "SELECT osp_url, osp_id, osp_nat, osp_chk, vpn_state, osp_regdate FROM site.osp_list_check_backup where osp_regdate >= curdate() order by osp_regdate desc;"
            curs.execute(sql)
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                    returnValue[key].append(result[i][2])
                    returnValue[key].append(result[i][3])
                    returnValue[key].append(result[i][4])
                    returnValue[key].append(result[i][5])
                else:
                    returnValue.update({key:[result[i][1],result[i][2],result[i][3],result[i][4],result[i][5]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

def startCrawling():
    getList =  getListDB()
    a = 0
    for k, i in getList.items():
        a = a + 1
        try:
            osp_url = k
            osp_id = i[0]
            osp_nat = i[1]
            osp_chk = i[2]
            vpn_state = i[3]
            osp_regdate = i[4].strftime('%Y-%m-%d %H:%M:%S')


            data = {
                'osp_id': osp_id,
                'osp_url' : osp_url,
                'osp_nat': osp_nat,
                'osp_chk': osp_chk,
                'vpn_state' : vpn_state,
                'osp_regdate' : osp_regdate
            }
            # print(data)
            # print("=================================")

            dbResult = insertALLDB(data)

        except:
            continue


if __name__=='__main__':
    start_time = time.time()

    print("vpn_osp_db 크롤링 시작")
    startCrawling()
    print("vpn_osp_db 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
