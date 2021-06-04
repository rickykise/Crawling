import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where user_idx in (22,23,24,25,26,27) and keyword_property="포함";'
        curs.execute(sql)
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][0]:{'add':[],'del':[]}})
        returnValue[result[i][0]]['add'] = getKeyword('포함',result[i][0],result[i][1],conn,curs)
        returnValue[result[i][0]]['del'] = getKeyword('제외',result[i][0],result[i][1],conn,curs)

    return returnValue

#Mrank 가져오기
def getUserIdx(keyword_main,conn,curs):

    with conn.cursor() as curs:
        sql = 'SELECT user_idx FROM keyword_data where keyword_main = %s;'
        curs.execute(sql, (keyword_main))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a == None
            return a

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'searchkeyword_data'
        data = {
            'user_idx' : args[0],
            'keyword_main' : args[1],
            'keyword' : args[2],
            'createDate' : now,
            'updateDate' : now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
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

def main(key):
    check = True
    print('검색어:', key)
    try:
        link = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=" + key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        html = driver.find_element_by_class_name("_related_keyword_ul").get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        li = soup.find_all('li')

        returnValue = []
        for item in li:
            searchWord = item.text.strip()
            returnValue.append(searchWord)

        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        keyword = ", ".join(returnValue)
        user_idx = getUserIdx(key,conn,curs)

        data = {
            'user_idx' : user_idx,
            'keyword_main' : key,
            'keyword' : keyword,
            'createDate' : now,
            'updateDate' : now
        }
        print(data)

        # try:
        #     curs = conn.cursor(pymysql.cursors.DictCursor)
        #     dbResult = insert(conn,user_idx,key,keyword,now,now)
        #     if dbResult:
        #         return False
        # finally :
        #     conn.close()

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 연관검색어 크롤링 시작")
    for k in dbKey.keys():
        main(k)
    print("네이버 연관검색어 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
