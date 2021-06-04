import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        i = 0;
        link = "https://dvdprime.com/g2/bbs/board.php?bo_table=movie&sca=&scrap_mode=&sfl=wr_subject&sop=and&stx="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_id("list_aside").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all("div", "relative list_table_row ")

        for item in div:
            pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = item.find('span', 'list_subject_span_pc').text.strip()
            if item.find('span', 'member'):
                writer = item.find('span', 'member').text.strip()
            if item.find('span', 'normal'):
                writer = item.find('span', 'normal').text.strip()
            timech = item.find('span', 'list_table_dates').text.strip()
            href = 'https://dvdprime.com' + item.find('a','list_subject_a')['href']
            board_number = href.split("&wr_id=")[1].split("&sca")[0]

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_id("view_Contents").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            contents = tags.find('div','resContents').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
            dateCheck = tags.find('div',id='view_datetime').text.strip().find('Updated')
            if dateCheck == -1:
                date = tags.find('div',id='view_datetime').text.strip()
            else:
                date = tags.find('div',id='view_datetime').text.strip().split("Updated at ")[1]
            timecheck = timech.find(':')
            if timecheck == -1: check=False;break
            print(timech)

            result = False;addKey = None
            mkey = getMainKeyword(dbKey,title)

            if mkey:
                paramKey = None
                addKey = dbKey[mkey]['add']
                if mkey == '공유' or mkey == '정유미': paramKey = mkey
                result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

            if result is False: break

            data = {
                'title' : title,
                'url' : href,
                'writer': writer,
                'writerIp': '',
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'dvdprime',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'dvdprime',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("dvdprime 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '마약왕':
        #     startCrawling(k)
        startCrawling(k)
    print("dvdprime 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
