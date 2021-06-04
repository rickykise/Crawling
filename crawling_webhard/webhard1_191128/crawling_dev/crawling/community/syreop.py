import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date, timedelta

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div', 'postBlock')

    date = div.find('div', 'block-clearhead').find('span', 'info_top').text.strip()
    if date.find('분')!= -1:
        datech = date.split("분")[0]
        datecheck = int(datech)
        now = datetime.datetime.now()
        date2 = now - datetime.timedelta(minutes=datecheck)
        date = date2.strftime('%Y-%m-%d %H:%M:00')
    elif date.find('시간')!= -1:
        if date.find('한 시간 전')!= -1:
            now = datetime.datetime.now()
            datech = now - datetime.timedelta(hours=1)
            date = datech.strftime('%Y-%m-%d %H:00:00')
        else:
            datech = date.split("시간")[0]
            datecheck = int(datech)
            now = datetime.datetime.now()
            date2 = now - datetime.timedelta(hours=datecheck)
            date = date2.strftime('%Y-%m-%d %H:00:00')
    else:
        pass

    if date.find('에') != -1:
        date = date.split("에")[0]

    contents = div.find('p').text.replace("\n","").replace("\t","").replace("\r","").replace("\xa0", "").strip()

    data = {
        'date': date,
        'contents' : contents
    }
    # print(data)
    return data

def startCrawling(key):
    i = 0;check = True
    print("키워드 : ",key)
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    while check:
        try:
            i = i+1
            link = "http://www.syreop.com/b/star?page="
            link2 = "&string="+key
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i)+link2)
            time.sleep(3)
            html = driver.find_element_by_id("mainContent").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            ul = soup.find_all("ul")[1]
            li = ul.find_all("li",class_=False)
            if len(li) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in li:
                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('span', 'title').text.strip()
                writer = item.find('span', 'nick').text.strip()
                timech = item.find('span', 'regdate').text.strip()
                url = 'http://www.syreop.com' + item.find('a', 'listBlock')['href']
                board_number = url.split("star/")[1].split("?string")[0]
                timecheck = timech.find('-')
                if timecheck != -1: check=False;break
                print(timech)
                resultData = getContents(url)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                data = {
                    'title' : title,
                    'url' : url,
                    'writer': writer,
                    'writerIp': '',
                    'board_number': board_number,
                    'contents' : resultData['contents'],
                    'date': resultData['date'],
                }
                # print(data)

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'syreop',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'syreop',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False
                finally :
                    conn.close()
                    conn2.close()
        except:
            pass

        finally:
            driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("syreop 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("syreop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
