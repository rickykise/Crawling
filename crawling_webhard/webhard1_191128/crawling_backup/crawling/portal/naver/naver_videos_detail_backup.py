#네이버 영화 예고편 저장소
import datetime,pymysql,time
import sys,os
import urllib.request
import requests,re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup

# url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = 'SELECT url FROM naver_videos_all where writeDate >= DATE_ADD(NOW(), INTERVAL -6 day) order by createDate desc;'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_videos_detail_backup'
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

def main(item):
    url = item
    print("url:", url)
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        link= url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        page_main = driver.find_element_by_class_name("end_container").get_attribute('innerHTML')
        tags = BeautifulSoup(page_main,'html.parser')

        conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        title = tags.find('div', 'watch_title').find('h3').text.strip()
        if title.find("'") != -1:
            portal_subtitle = tags.find('div', 'watch_title').find('h3').text.strip().split("'")[1].split("'")[0]
        elif title.find("<") != -1:
            portal_subtitle = tags.find('div', 'watch_title').find('h3').text.strip().split("<")[1].split(">")[0]
        else:
            portal_subtitle = ''
        board_number = link.split("v/")[1]
        dateCheck = tags.find('div', 'video_watch open').find('div', 'title_info').find('span','date').text.strip().split("등록")[1]
        datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M')
        date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M')
        view = tags.find('div', 'title_info').find('span','play').text.strip().split("재생수")[1]
        view_cnt = int(''.join(list(filter(str.isdigit,view))))
        if tags.find('div', 'watch_btn').find('em','u_cnt _cnt').text.strip() == '':
            like_cnt = 0
        else:
            like = tags.find('div', 'watch_btn').find('em','u_cnt _cnt').text.strip()
            like_cnt = int(''.join(list(filter(str.isdigit,like))))
        if tags.find('div', 'watch_btn').find('span','count _commentCount').text.strip() == '':
            reply_cnt = 0
        else:
            reply = tags.find('div', 'watch_btn').find('span','count _commentCount').text.strip()
            reply_cnt = int(''.join(list(filter(str.isdigit,reply))))

        data = {
            'portal_title' : title,
            'portal_subtitle' : portal_subtitle,
            'portal_writer' : '네이버영화',
            'url' : link,
            'like_cnt' : like_cnt,
            'reply_cnt' : reply_cnt,
            'view_cnt' : view_cnt,
            'writeDate' : date,
            'board_number' : board_number,
            'createDate' : now,
            'updateDate' : now
        }
        print(data)

        # conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
        # try:
        #     curs = conn.cursor(pymysql.cursors.DictCursor)
        #     dbResult = insert(conn,data['portal_title'],data['portal_subtitle'],data['portal_writer'],data['url'],data['like_cnt'],data['reply_cnt'],data['view_cnt'],data['writeDate'],data['board_number'],data['createDate'],data['updateDate'])
        #     if dbResult:
        #         return False
        # finally :
        #     conn.close()
    # except:
    #     pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("네이버영화 동영상 크롤링 시작")
    for u in getUrl:
        main(u)
    print("네이버영화 동영상 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
