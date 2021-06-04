# 네이버 검색 Open API - 카페 검색
import os,sys
from portal_api import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime,time,pymysql

def cafeCheck(link,keyword,starKey):
    result = False
    delURL = ['apaqjshfdlghdqhtmzk','daum']

    if  link.find('joonggonara') != -1 and any(keyword == s for s in starKey) or\
        link.find('/heartofdarkness/') != -1 and any(keyword == s for s in starKey) or\
        link.find('/jinshhop/') != -1 and any(keyword == s for s in starKey) or\
        link.find('/specup/') != -1 and keyword == '아이유' or\
        any(link.find(s) != -1 for s in delURL):
        result = True

    return result

def startCrawling(key):
    apiStartNum = 1;insertNum = 0;paramKey = None;check=False;dic = []
    if key == '공유' or key == '정유미': paramKey = key
    key = '미니카'
    print("키워드 : "+key)
    while apiStartNum < 200:
        data = searchNAPI('cafearticle',key,'50',str(apiStartNum),'date')
        print(data)
        print("============================")
        # if apiStartNum > data['total']: break
        # for item in data['items']:
        #     # if cafeCheck(item['link'],key,starKey): continue
        #     item['title'] = setText(item['title'],0) # 제목
        #     item['description'] = setText(item['description'],1) # 내용
        #     # result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
        #     # if result:
        #     conn = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
        #     try:
        #         curs = conn.cursor(pymysql.cursors.DictCursor)
        #         item['title'] = (len(item['title']) > 50) and item['title'][:47]+"…" or item['title']
        #         date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #         putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
        #         putKeyType = getPutKeywordType(putKey,conn,curs)
        #         putKeyType = (putKeyType == None) and ' ' or putKeyType
        #
        #
        #         print(item)
        #         print(item['title'])
        #         print(item['description'])
        #         print("============================")
        #         # dbResult = insert(conn,'cafe','naver',item['title'],'',date,dbKey[key]['add'][0],putKey,putKeyType,item['link'])
        #
        #         if dbResult:
        #             check=True;break
        #         else:
        #             dic.append({'keyword':putKey,'url':item['link']})
        #             insertNum = insertNum+1
        #     finally:
        #         conn.close()
        if check: break
        apiStartNum = apiStartNum + 50
    if dic:
        getWriter(dic,'naver','cafe')
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    starKey = getStarWachKey(conn,curs)
    conn.close()
    print("네이버 카페 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("네이버 카페 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
