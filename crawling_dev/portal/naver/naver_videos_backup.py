#네이버 영화 예고편 저장소
import datetime,pymysql,time
import sys,os
import urllib.request
import requests,re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_videos'
        data = {
            'portal_title' : args[0],
            'portal_subtitle' : args[1],
            'portal_writer' : args[2],
            'url' : args[3],
            'like_cnt' : args[4],
            'reply_cnt' : args[5],
            'share_cnt' : 0,
            'view_cnt' : args[6],
            'writeDate' : args[7],
            'board_number' : args[8],
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
        sql = "SELECT like_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
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
        sql = "SELECT reply_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
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
        sql = "SELECT view_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
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

# 등록날짜 가져오는 함수
def getCreateDate(url,create1,create2,conn,curs):
    check = False

    with conn.cursor() as curs:
        sql = "SELECT portal_title FROM naver_videos where url = %s and createDate >= %s and createDate <= %s;"
        curs.execute(sql, (url,create1,create2))
        result = curs.fetchone()
        # print('접속')
        if result != None:
            check = True
            return check
        else:
            return check

# def getContents(url):
#     r = requests.get(url)
#     c = r.content
#     soup = BeautifulSoup(c,"html.parser")
#     div = soup.find('div', 'end_container')
#
#     dateCheck = div.find('div', 'video_watch open').find('div', 'title_info').find('span','date').text.strip().split("등록")[1]
#     date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M:%S')
#     if div.find('div', 'watch_btn').find('span','count _commentCount').text.strip() == '':
#         reply_cnt = 0
#     else:
#         reply = div.find('div', 'watch_btn').find('span','count _commentCount').text.strip()
#         reply_cnt = int(''.join(list(filter(str.isdigit,reply))))
#
#     data = {
#         'reply_cnt' : reply_cnt,
#         'writeDate' : date
#     }
#     # print(data)
#     return data

def startCrawling():
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        link = 'http://tv.naver.com/navermovie/clips'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        for i in range(0, 3) :
            try:
                driver.find_element_by_xpath('//*[@id="cds_flick"]/div/div[3]/div/div/div/div[2]/div[3]/a').click()
                time.sleep(3)
                i +=1
            except:
                break
        html = driver.find_element_by_class_name("cds_flick").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all('div',  class_='_MM_CARD')

        for items in div:
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = items.find('dt', 'title').find('a').text.replace("#","")
            if title.find("'") != -1:
                portal_subtitle = items.find('dt', 'title').find('a').text.replace("#","").split("'")[1].split("'")[0]
            elif title.find("<") != -1:
                portal_subtitle = items.find('dt', 'title').find('a').text.replace("#","").split("<")[1].split(">")[0]
            else:
                portal_subtitle = ''
            view = items.find('dd', 'meta').find('span', 'hit').text.split("수")[1]
            view_cnt = int(''.join(list(filter(str.isdigit,view))))
            like = items.find('dd', 'meta').find('span', 'like').text.split("수")[1]
            like_cnt = int(''.join(list(filter(str.isdigit,like))))
            timech = items.find('dd', 'meta').find('span', 'time').text
            # print(timech)
            href = 'http://tv.naver.com' + items.find('dt', 'title').find('a')['href']
            board_number = href.split("v/")[1]
            if timech == '1주 전':
                break
            driver.get(href)
            time.sleep(3)
            page_main = driver.find_element_by_class_name("end_container").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')

            dateCheck = tags.find('div', 'video_watch open').find('div', 'title_info').find('span','date').text.strip().split("등록")[1]
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M:%S')
            if tags.find('div', 'watch_btn').find('span','count _commentCount').text.strip() == '':
                reply_cnt = 0
            else:
                reply = tags.find('div', 'watch_btn').find('span','count _commentCount').text.strip()
                reply_cnt = int(''.join(list(filter(str.isdigit,reply))))
            # resultData = getContents(href)

            data = {
                'portal_title' : title,
                'portal_subtitle' : portal_subtitle,
                'portal_writer' : '네이버영화',
                'url' : href,
                'like_cnt' : like_cnt,
                'reply_cnt' : reply_cnt,
                'view_cnt' : view_cnt,
                'writeDate' : date,
                'board_number' : board_number,
                'createDate' : now,
                'updateDate' : now
            }
            # print(data)

            getView = getSearchView(data['url'],conn,curs)
            getLike = getSearchLike(data['url'],conn,curs)
            getReply = getSearchReply(data['url'],conn,curs)

            m_view = data['view_cnt'] - getView
            m_like = data['like_cnt'] - getLike
            m_reply = data['reply_cnt'] - getReply

            create1 = datetime.datetime.now().strftime('%Y-%m-%d %H:00:00')
            create2 = datetime.datetime.now().strftime('%Y-%m-%d %H:59:59')
            GetCreateDate = getCreateDate(data['url'],create1,create2,conn,curs)
            # print(GetCreateDate)
            if GetCreateDate == False:
                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['portal_title'],data['portal_subtitle'],data['portal_writer'],data['url'],data['like_cnt'],data['reply_cnt'],data['view_cnt'],data['writeDate'],data['board_number'],data['createDate'],data['updateDate'])
                    insert2(conn,data['url'],m_view,m_like,m_reply,data['writeDate'],data['createDate'],data['updateDate'])
                    if dbResult:
                        return False
                finally :
                    conn.close()
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("네이버영화 동영상 크롤링 시작")
    startCrawling()
    print("네이버영화 동영상 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
