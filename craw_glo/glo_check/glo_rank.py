import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup as bs

def insertALL(data):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['osp_id'],data['osp_url'],data['osp_nat'],data['osp_rank'])
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
        tableName = 'osp_rank'
        data = {
            'osp_id': args[0],
            'osp_url': args[1],
            'osp_nat': args[2],
            'osp_rank': args[3],
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

# url 가져오는 함수
def getOsp():
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "SELECT osp_url, osp_id, osp_nat FROM osp_list where osp_state = '1' order by n_idx asc;"
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

        return returnValue

def startCrawling():
    getUrl = getOsp()
    for url, osp in getUrl.items():
        getUrl = url.replace('https://', '').replace('http://', '')
        with requests.Session() as s:
            link = "https://www.alexa.com/siteinfo/" + getUrl
            try:
                post_one  = s.get(link)
                soup = bs(post_one.text, 'html.parser')
                if soup.find('div', 'rank-global'):
                    rank = soup.find('div', 'rank-global').find('p', 'big data').text.replace('#', '').replace(',', '').replace(' ', '').strip()
                    rank = int(rank)

                    data = {
                        'osp_id': osp[0],
                        'osp_url': url,
                        'osp_nat': osp[1],
                        'osp_rank': rank
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
                else:
                    continue
                    # rank = None

                # data = {
                #     'osp_id': osp[0],
                #     'osp_url': url,
                #     'osp_nat': osp[1],
                #     'osp_rank': rank
                # }
                # # print(data)
                # # print("=================================")
                #
                # dbResult = insertALL(data)
            except:
                # data = {
                #     'osp_id': osp[0],
                #     'osp_url': url,
                #     'osp_nat': osp[1],
                #     'osp_rank': None
                # }
                # # print(data)
                # # print("=================================")
                #
                # dbResult = insertALL(data)
                continue

if __name__=='__main__':
    start_time = time.time()

    print("alexa_rank 크롤링 시작")
    startCrawling()
    print("alexa_rank 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
