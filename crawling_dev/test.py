import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

# 제외,포함검색어 가져오는 함수
def getKeyword(prop,kmain,idx,conn,curs):
    rKeyword = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword FROM keyword_data WHERE user_idx = %s and keyword_main=%s and keyword_property = %s;'
        curs.execute(sql, (idx,kmain,prop))
        returnValue = curs.fetchall()
        rKeyword = []
        if prop == '포함':
            rKeyword.append(kmain)
        for i in range(len(returnValue)):
            rKeyword.append(str(returnValue[i]).replace("(","").replace(")","").replace(",","").replace("\'",""))
    return rKeyword

# 검색키워드 가져오는 함수
def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where keyword_property=%s and user_idx in (22,23,24,25,26,27) and user_idx != 21;'
        curs.execute(sql, ('포함'))
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][0]:{'add':[],'del':[]}})
        returnValue[result[i][0]]['add'] = getKeyword('포함',result[i][0],result[i][1],conn,curs)
        returnValue[result[i][0]]['del'] = getKeyword('제외',result[i][0],result[i][1],conn,curs)

    with conn.cursor() as curs:
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and not user_idx in (22,23,24,25,26,27) and user_idx != 21 and keyword_type!=%s and keyword is not null;"
        curs.execute(sql,('포함',''))
        result = curs.fetchall()

    for i in range(len(result)):
        returnValue.update({result[i][1]:{'add':[],'del':[]}})
        returnValue[result[i][1]]['add'] = getKeyword('포함',result[i][0],result[i][2],conn,curs)
        returnValue[result[i][1]]['del'] = getKeyword('제외',result[i][0],result[i][2],conn,curs)

    return returnValue

# 내용 키워드 체크
def checkKeyword(title,text,add,delete,keyword=None):
    print(delete)
    textResult = None
    titleResult = None

    if text:
        if any(text.find(s.replace("영화","")) != -1 for s in add):
            if all(text.find(s) == -1 for s in delete):
                textResult = True
            else:
                textResult = False
        else:
            textResult = False
    if title:
        if any(title.find(s.replace("영화","")) != -1 for s in add):
            if all(title.find(s) == -1 for s in delete):
                titleResult = True
            else:
                titleResult = False
        else:
            titleResult = False

    returnVal = textResult or titleResult
    if keyword:
        returnVal = textResult and titleResult

    return returnVal

def startCrawling(key):
    print("키워드 : ",key)
    result = checkKeyword('l눌러서구매하기ㅣ:l오늘의힐링_쇼핑l (추천) 최저가 공유', '',dbKey[key]['add'],dbKey[key]['del'],'')
    print(result)


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("test 크롤링 시작")
    for k in dbKey.keys():
        if k == "공유":
            startCrawling(k)
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
