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

def startCrawling(site):
    with requests.Session() as s:
        safe_req = s.post('http://www.filemaru.com/proInclude/ajax/safezonePrc.php', data=Safe)
        i = 0;check = True
        link = "http://www.filemaru.com/?doc=list_sub&cate="+site+"&subCate=&sort=&listCnt=25&adtChk=&searchType=&searchVal=&p="
        while check:
            i = i+1
            if i == 4:
                break
            r = s.get(link+str(i))
            # time.sleep(2)
            soup = bs(r.text, 'html.parser')
            # print(soup)
            table = soup.find('table', 'sbase_list')
            tr = table.find("tbody").find_all("tr", "choiceViewTr")
            # try:
            for item in tr:
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

                title = text.split('fileTitle" : "')[1].split('"')[0]

                cnt_price = text.split('filePoint" : "')[1].split('"')[0].replace(",","")
                cnt_writer = text.split('fileRegNick" : "')[1].split('"')[0]
                cnt_vol = text.split('fileSize" : "')[1].split('"')[0]
                cnt_fname = text.split('fileName" : "')[1].split('"')[0]
                if text.find('files') != -1:
                    cnt_fname = text.split('fileName" : "')[2].split('"')[0]
                # cnt_chk = text.split('fileTitle" : "')[1].split('"')[0]

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
                print(data)

                conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    if dbResult == True:
                        print('있는 파일이다')
                finally :
                    conn.close()
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("filemaru 크롤링 시작")
    site = ['','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("filemaru 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
