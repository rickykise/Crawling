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
        # sql = 'SELECT url FROM media_data where writeDate >= DATE_ADD(NOW(), INTERVAL -1 day) order by createDate asc;'
        sql = 'SELECT url FROM media_data where writeDate >= curdate() and v_state=0 order by createDate asc;'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def main(item):
    url = item
    print("url:", url)
    insertNum = 0;paramKey = None;check = False
    v_state = 1

    try:
        link = url
        r = requests.get(link)
        c = r.text
        soup = BeautifulSoup(c,'html.parser')

        #naver
        if soup.find('div', 'vod_area'):
            if soup.find('div', 'content').find('div', 'vod_area').find('iframe')['title'] == '영상 플레이어':
                print('비디오')
                v_state = 2
            else:
                v_state = 1
        #daum
        elif soup.find('div', 'video_frm'):
            contents = soup.find('div', 'video_frm')
            iframe = contents.find('iframe','player_iframe')
            if iframe != None:
                print('비디오')
                v_state = 2
            else:
                v_state = 1
        #kbs
        elif soup.find('div', 'landing-box'):
            div = soup.find('div', 'landing-box').find('div', id='YTN_Player')
            if div != None:
                print('비디오')
                v_state = 2
            else:
                v_state = 1
        #ytn
        elif soup.find('div', id='YTN_Player'):
            div = soup.find('div', id='YTN_Player')
            if div != None:
                print('비디오')
                v_state = 2
            else:
                v_state = 1

        conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            sql = "update media_data set v_state=%s, updateDate=%s where v_state=0 and url =%s;"
            curs.execute(sql,(v_state, now, link))
            conn.commit()
        finally:
            conn.close()
    except:
        pass

    print(v_state)

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("미디아 비디오 체크 크롤링 시작")
    for u in getUrl:
        main(u)
    print("미디아 비디오 체크 크롤링 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
