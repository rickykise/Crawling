import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

Safe = {
    'safe': 'on'
}

conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

def startCrawling(key):
    with requests.Session() as s:
        print('키워드: ',key)
        safe_req = s.post('http://www.filemaru.com/proInclude/ajax/safezonePrc.php', data=Safe)
        i = 5;a = 0;insertNum = 0;check = True
        link = "http://www.filemaru.com/?doc=list_sub&cate=&subCate=&sort=&listCnt=200&adtChk=&searchType=all&section=&searchVal="+key+"&p="
        while check:
            # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # endTimea = datetime.datetime.now() + datetime.timedelta(minutes=5)
            # endTime = endTimea.strftime('%Y-%m-%d %H:%M:%S')
            # endTime = '2019-01-18 10:40:00'
            # if now > endTime:
            #     break
            try:
                i = i+1
                print('페이지: ',i)
                if i == 50:
                    break
                r = s.get(link+str(i))
                soup = bs(r.text, 'html.parser')
                searcht = str(soup)
                if searcht.find('검색어에') != -1:
                    print('게시물이 없습니다.')
                    break
                table = soup.find('table', 'sbase_list')
                tr = table.find("tbody").find_all("tr", class_=None)
                if len(tr) <= 2:
                    print('게시물이 없습니다.')
                    break
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                print('=====================================================')

                for item in tr:
                    a = a+1
                    if a == 201:
                        a = 1
                    if a < 10:
                        print('0',str(a),'번 째 게시글')
                    else:
                        print(a,'번 째 게시글')
                    cnt_num = item.find('input')['idx']
                    url = 'http://www.filemaru.com/proInclude/ajax/view.php'
                    url2 = "http://www.filemaru.com/proInclude/ajax/view.php?idx="+cnt_num
                    Page = {
                        'idx': cnt_num
                    }
                    post_one  = s.post(url, data=Page)
                    soup = bs(post_one.text, 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    try:
                        title = text.split('fileTitle" : "')[1].split('"')[0]
                        cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")
                        cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                        cnt_vol = text.split('fileSize" : "')[1].split('"')[0]
                        cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                        if text.find('files') != -1:
                            cnt_fname = text.split('fileName" : "')[2].split('"')[0]
                        # cnt_chk = text.split('fileTitle" : "')[1].split('"')[0]
                    except Exception as e:
                        print("에러 : ",e)
                        continue

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemaru',
                        'Cnt_title': title,
                        'Cnt_url': url2,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print('========================================================================')

                    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        if dbResult == True:
                            continue
                        else:
                            insertNum = insertNum+1
                    finally :
                        conn.close()
            except Exception as e:
                print("===========에러==========\n에러 : ",e,"\n===========에러==========")
                continue
        print("insert : ",insertNum)
        print('==================================================================')

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("filemaru 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
