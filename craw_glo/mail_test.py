import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['webhard'],data['title'],data['date'],data['cnt_num'],data['num'])
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
        tableName = 'mail_Get'
        data = {
            'webhard': args[0],
            'title': args[1],
            'date': args[2],
            'cnt_num': args[3],
            'num': args[4],
            'createDate': now
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

headers = {
    'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'ko-KR',
    'Connection':'Keep-Alive',
    'Cookie':'WMSESSION=ATAAz%2F9c3JixQrGjjoo9uvZJQeYEhsaxlRuftKCZ2wf%2FJgJhddBfrXogzeV%2F8Hjchec4x3A%3D',
    'Host':'webmail.unionc.kr',
    'Referer':'http://webmail.unionc.kr/intro.php',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True; dateSUm = 'startDate=2021-03-15&endDate=2021-03-21'; key = 'filesun'
    while check:
        if i == 300:
            break
        if i == 0:
            r = requests.get('http://webmail.unionc.kr/user/mail/main.php?page=list&'+dateSUm+'&mbox=&keyField=&keyWord='+key, headers=headers)
        else:
            r = requests.get('http://webmail.unionc.kr/user/mail/main.php?page=list&'+dateSUm+'&mbox=&keyField=&keyWord='+key+'&start='+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        i = i+100
        tr = soup.find('table', 'eChkColor').find('tbody').find_all('tr')

        # [filemong:나의 살던 고향은] KBS미디어의 저작권물(게시물:2857232)의 처리 요청 드립니다. - 3차
        for item in tr:
            title = item.find('a', 'ellipsis goto-read').text.strip()
            date = item.find_all('td')[4].text.strip()
            cnt_num = title.split('게시물:')[1].split(')')[0].strip()
            num = title.split('. -')[1].split('차')[0].strip()

            # 웹하드 	제목	날짜	게시물번호 	회차
            data = {
                'webhard': key,
                'title': title,
                'date': date,
                'cnt_num' : cnt_num,
                'num': num
            }
            # print(data)
            # print("=================================")

            dbResult = insertALL(data)



if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("메일 크롤링 시작")
    startCrawling()
    print("메일 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
