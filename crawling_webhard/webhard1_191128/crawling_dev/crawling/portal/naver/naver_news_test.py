# 네이버 검색 Open API - 뉴스 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from bs4 import BeautifulSoup
import datetime,time,pymysql

# 메인 키워드 가져오는 함수
def getMainNewsKeyword(conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT k_main,k_sub,k_type FROM keyword_mail;'
        curs.execute(sql)
        result = curs.fetchall()


        returnValue = {}
        for i in range(len(result)):
            media = result[i][0].replace("\ufeff","")
            if media in returnValue:
                returnValue[media].append(result[i][1])
            else:
                returnValue.update({media:[result[i][1]]})
        # print(returnValue)

        return returnValue

# 메인 타이틀 키워드 가져오는 함수
def getMainTileKeyword(conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT k_type_str,k_type FROM keyword_mail group by k_type_str;'
        curs.execute(sql)
        result = curs.fetchall()


        returnValue = {}
        for i in range(len(result)):
            media = result[i][0].replace("\ufeff","")
            if media in returnValue:
                returnValue[media].append(result[i][1])
            else:
                returnValue.update({media:[result[i][1]]})
        # print(returnValue)

        return returnValue

#내용 체크
def checkMainNewsKeyword(content, newsKey):
    returnValue = {
        'm' : None,
        'r' : None
    }

    for s in newsKey.keys():
        if content.find(s) != -1 :
            for m in newsKey[s]:
                if content.find(m) != -1 :
                    returnValue['m'] = m
                    returnValue['r'] = s


    return returnValue

#타이틀키 체크
def checkMaintitle_key(title_key, newsKey):
    returnValue = {
        'm' : None,
        'r' : None
    }

    for s in newsKey.keys():
        if title_key.find(s) != -1 :
            for m in newsKey[s]:
                if title_key.find(m) != -1 :
                    returnValue['m'] = m
                    returnValue['r'] = s


    return returnValue

#key_type 가져오기
def getSearchKeytpe(k_sub,k_main,conn,curs):

    with conn.cursor() as curs:
        sql = 'SELECT k_type FROM keyword_mail where k_sub = %s and k_main = %s limit 1;'
        curs.execute(sql, (k_sub,k_main))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a == None
            return a

# 서브뉴스키워드 가져오는 함수
def getSubNewsKeyword(conn, curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT k_sub FROM keyword_mail;'
        curs.execute(sql)
        result = curs.fetchall()
        k_sub = [i[0] for i in result]
        # print(swearword)
        return k_sub

def main(item):
    url = item
    # print("url:", url)
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
    getMainTileKeyworda = getMainTileKeyword(conn,curs)
    content = '캐스팅'
    contents  = content.replace("\n","").replace("\t","").replace("\xa0", "").replace("\xed", "")
    title_key = '경쟁영화'
    news_keyword = checkMainNewsKeyword(content, getMainNewsKeyworda)

    # news_keyword = checkMaintitle_key(title_key, getMainTileKeyworda)
    # print(news_keyword['s'])

    news_keyword = checkMainNewsKeyword(contents, getMainNewsKeyworda)
    if news_keyword != None:
        k_type = getSearchKeytpe(news_keyword['m'],news_keyword['r'],conn,curs)
        print(k_type)

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getK = getSubNewsKeyword(conn,curs)
    conn.close()
    for u in getK:
        main(u)
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
