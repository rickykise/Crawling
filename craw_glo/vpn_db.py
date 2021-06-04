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
    if data['cnt_writer'] == '':
        data['cnt_writer'] = None
    if data['host_cnt'] == '':
        data['host_cnt'] = '1'

    try:
        if data['site_p_img'] == None:
            data['site_p_img'] = None
            data['site_r_img'] = None
            data['site_img_chk'] = None
    except:
        data['site_p_img'] = None
        data['site_r_img'] = None
        data['site_img_chk'] = None

    try:
        if data['origin_url'] == None:
            data['origin_url'] = None
            data['origin_osp'] = None
    except:
        data['origin_url'] = None
        data['origin_osp'] = None

    try:
        if data['cnt_cate'] == None:
            data['cnt_cate'] = None
    except:
        data['cnt_cate'] = None


    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['cnt_id'],data['cnt_osp'],data['cnt_title'],data['cnt_title_null'],data['host_url'],data['host_cnt'],data['site_url'],data['cnt_cp_id'],data['cnt_keyword'],data['cnt_nat'],data['cnt_regdate'],data['cnt_writer'],data['cnt_cate'],data['origin_url'],data['origin_osp'],data['site_p_img'],data['site_r_img'],data['site_img_chk'])
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
        tableName = 'cnt_f_list'
        data = {
            'cnt_id': args[0],
            'cnt_osp': args[1],
            'cnt_title': args[2],
            'cnt_title_null': args[3],
            'host_url': args[4],
            'host_cnt': args[5],
            'site_url': args[6],
            'cnt_cp_id': args[7],
            'cnt_keyword': args[8],
            'cnt_nat': args[9],
            'cnt_regdate': args[10],
            'cnt_regdate2': None,
            'cnt_chk': '0',
            'cnt_f_chk': '0',
            'cnt_writer': args[11],
            'cnt_cate': args[12],
            'cnt_img_chk': '0',
            'origin_url': args[13],
            'origin_osp': args[14],
            'site_p_img': args[15],
            'site_r_img': args[16],
            'site_img_chk': args[17]
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

def dbDelete(n_idx):
    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "delete from cnt_f_list_vpn where n_idx=%s;"
    curs.execute(sql,(n_idx))
    conn.commit()


# backupDB 가져오는 함수
def getListDB():
    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    result = None
    with conn.cursor() as curs:
        try:
            sql = "SELECT n_idx, cnt_id, cnt_osp, cnt_title, cnt_title_null, host_url, site_url, cnt_keyword, cnt_nat, cnt_regdate FROM site.cnt_f_list_vpn where cnt_regdate >= curdate() order by cnt_regdate desc;"
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
                    returnValue[key].append(result[i][6])
                    returnValue[key].append(result[i][7])
                    returnValue[key].append(result[i][8])
                    returnValue[key].append(result[i][9])
                else:
                    returnValue.update({key:[result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7],result[i][8],result[i][9]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

def startCrawling():
    getList =  getListDB()
    for k, i in getList.items():
        try:
            n_idx = k
            cnt_id = i[0]
            cnt_osp = i[1]
            title = i[2]
            title_null = i[3]
            host_url = i[4]
            url = i[5]
            cnt_keyword = i[6]
            cnt_nat = i[7]
            cnt_regdate = i[8].strftime('%Y-%m-%d %H:%M:%S')

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : cnt_osp,
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': cnt_nat,
                'cnt_regdate': cnt_regdate,
                'cnt_writer': ''
            }
            # print(n_idx)
            # print(data)
            # print("=================================")

            dbResult = insertALLDB(data)

            # dbDel = dbDelete(n_idx)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()

    print("vpn_db 크롤링 시작")
    startCrawling()
    print("vpn_db 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
