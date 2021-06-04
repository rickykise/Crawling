#네이버 영화 예고편 그래프
import datetime,pymysql,time
import sys,os
import urllib.request
import requests,re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert2(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_graph'
        data = {
            'url' : args[0],
            'view_cnt' : args[1],
            'like_cnt' : args[2],
            'reply_cnt' : args[3],
            'writeDate' : args[4],
            'createDate' : args[5],
            'updateDate' : args[6]
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

# url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT url FROM naver_videos where createDate >= '2018-10-11 08:00:00' and createDate <= '2018-10-11 08:59:59' order by createDate desc"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# writeDate 가져오는 함수
def getSearchWrite(url,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT writeDate FROM naver_videos where url = %s limit 1;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 좋아요수 가져오는 함수
def getSearchLike(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT like_cnt FROM naver_videos where createDate >= '2018-10-11 09:00:00' and createDate <= '2018-10-11 09:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 댓글수 가져오는 함수
def getSearchReply(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT reply_cnt FROM naver_videos where createDate >= '2018-10-11 09:00:00' and createDate <= '2018-10-11 09:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 조회수 가져오는 함수
def getSearchView(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT view_cnt FROM naver_videos where createDate >= '2018-10-11 09:00:00' and createDate <= '2018-10-11 09:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a


# 좋아요수2 가져오는 함수
def getSearchLike2(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT like_cnt FROM naver_videos where createDate >= '2018-10-11 08:00:00' and createDate <= '2018-10-11 08:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 댓글수2 가져오는 함수
def getSearchReply2(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT reply_cnt FROM naver_videos where createDate >= '2018-10-11 08:00:00' and createDate <= '2018-10-11 08:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 조회수2 가져오는 함수
def getSearchView2(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT view_cnt FROM naver_videos where createDate >= '2018-10-11 08:00:00' and createDate <= '2018-10-11 08:59:59' and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

def main(item):
    url = item
    print("url:", url)
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    writeDate = getSearchWrite(url,conn,curs)
    date = writeDate.strftime('%Y-%m-%d %H:%M:%S')

    getView = getSearchView(url,conn,curs)
    getLike = getSearchLike(url,conn,curs)
    getReply = getSearchReply(url,conn,curs)

    getView2 = getSearchView2(url,conn,curs)
    getLike2 = getSearchLike2(url,conn,curs)
    getReply2 = getSearchReply2(url,conn,curs)

    m_view = getView - getView2
    m_like = getLike - getLike2
    m_reply = getReply - getReply2

    data = {
        'url' : url,
        'writeDate' : date,
        'createDate' : '2018-10-11 09:17:32',
        'updateDate' : '2018-10-11 09:17:32'
    }

    print(data)

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert2(conn,data['url'],m_view,m_like,m_reply,data['writeDate'],data['createDate'],data['updateDate'])
        if dbResult:
            return False
    finally :
        conn.close()
    conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
    try:
        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
        dbResult = insert2(conn2,data['url'],m_view,m_like,m_reply,data['writeDate'],data['createDate'],data['updateDate'])
        if dbResult:
            return False
    finally :
        conn2.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("네이버영화 그래프 크롤링 시작")
    for u in getUrl:
        main(u)
    print("네이버영화 그래프 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
