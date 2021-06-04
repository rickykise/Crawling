import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs


conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',port=3306,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#DB 업데이트 함수
def dbUpdate(textType,url,keyword):
    sql = "update portal_data set textType=%s where url=%s and keyword=%s; "
    curs.execute(sql,(textType,url,keyword))
    conn.commit()

# url 가져오는 함수
def getSearchUrl():
    with conn.cursor() as curs:
        sql = "select url, keyword from portal_data where title_key = '닥터프리즈너' and textType is null;"
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

# url 가져오는 함수
def getKeyword():
    result = None
    with conn.cursor() as curs:
        sql = "SELECT url, keyword FROM kbs_test;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})

        return returnValue

def checkUrl(url, keyword, getKeyword):
    returnValue = {
        'u' : None,
        'k' : None
    }

    for s, d in getKeyword.items():
        if url.find(s) != -1 :
            returnValue['u'] = s
            # print(d[0])
            # print('==========================')
            if keyword[0].find(d[0]) != -1:
                returnValue['k'] = d[0]
            else:
                returnValue['u'] = None

    return returnValue

def getText(url, keyword):
    with conn.cursor() as curs:
        sql = "select textType from kbs_test where url=%s and keyword=%s;"
        curs.execute(sql,(url, keyword))
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a


def main(url, keyword):
    getKey = getKeyword()
    keyCheck = checkUrl(url, keyword, getKey)
    if keyCheck['u'] != None:
        textType = getText(keyCheck['u'], keyCheck['k'])
        print(keyCheck['u'])
        print(keyCheck['k'])
        print(textType[0])
        print('==============================')
        dbUpdate(textType[0],keyCheck['u'],keyCheck['k'])

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl()
    print("test check 크롤링 시작")
    for u, c in getUrl.items():
        main(u, c)
    print("test check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
