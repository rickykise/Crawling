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
        link = "http://www.dogdrip.net/?_filter=search&mid=userdog&category=&search_target=title&search_keyword="+key+"&page="
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("container ").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table', 'table-divider')
        tr = table.find("tbody").find_all("tr")

        for item in tr:
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'notice') != None:
                continue
            title = item.find('td', 'title').find('a').find('span', 'title-link').text.strip()
            writer = item.find('td', 'author').text.strip()
            timech = item.find('td', 'time').text.strip()
            hrefch = item.find('td', 'title').find('a')['href']
            board_number = hrefch.split("document_srl=")[1].split("&page")[0]
            href = 'http://www.dogdrip.net/'+board_number

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("container").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            contents = tags.find('div',id='article_1').text.strip().split("개드립으로")[0].replace("\n","").replace("\t","").replace("\xa0", "")
            # dateCheck = tags.find('div','date').text.strip()
            # datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            # date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
            timecheck = timech.find('분 전')
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
            conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'dogdrip',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'dogdrip',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("dogdrip 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("dogdrip 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
