import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)


#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['title'],data['url'],data['d_url'],data['d_num'])
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
        tableName = 'dint_sbs_list'
        data = {
            'title': args[0],
            'url': args[1],
            'd_url': args[2],
            'd_num': args[3]
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
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Host': 'www.dint.co.kr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True;a= 0
    link = 'http://www.dint.co.kr/shop/shopbrand.html?type=Y&xcode='+site+'&sort=&page='
    if site == "024&mcode=001":
        a = 85
    else:
        a = 5
    while check:
        i = i+1
        if i == 85:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li', 'item-list')

        try:
            for item in li:
                title = item.find('div', 'over_text_wrap').find('div').text.strip()
                titleCheck = title.lower()
                if titleCheck.find('sbs') != -1:
                    url = 'http://www.dint.co.kr'+item.find('a')['href']

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    if soup.find('div', 'over_text_wrap'):
                        continue

                    li = soup.find('ul', 'slides').find_all('li')
                    d_num = 1
                    for item in li:
                        d_url = item.find('img')['src']

                        data = {
                            'title': title,
                            'url': url,
                            'd_url': d_url,
                            'd_num': d_num
                        }
                        # print(data)
                        # print("=================================")

                        d_num = d_num + 1

                        dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()

    print("dint 크롤링 시작")
    # site = ['045&mcode=035','024&mcode=001']
    site = ['024&mcode=001']
    for s in site:
        startCrawling(s)
    print("dint 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
