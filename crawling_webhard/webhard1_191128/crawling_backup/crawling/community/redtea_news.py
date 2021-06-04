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
        link = "https://redtea.kr/pb/pb.php?id=news&ss=on&keyword="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("bbs_wrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table', 'list')
        tr = table.find('tbody').find_all('tr', 'listtr')

        for item in tr:
            pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'tdnum').text.strip() == '공지':
                continue
            if item.find('td', 'tdsub old'):
                title = item.find('td', 'tdsub old').find('a').find('span', 'subj').text.strip()
                href= "https://redtea.kr/pb/" + item.find('td', 'tdsub old').find('a')['href']
            elif item.find('td', 'tdsub new'):
                title = item.find('td', 'tdsub new').find('a').find('span', 'subj').text.strip()
                href= "https://redtea.kr/pb/" + item.find('td', 'tdsub new').find('a')['href']
            writer = item.find('td', 'tdname').text.strip()
            timech = item.find('td', 'tddate').text.strip()
            datetime.datetime.strptime(timech, "%y/%m/%d").strftime('%y/%m/%d')
            datech = datetime.datetime.strptime(timech, "%y/%m/%d").strftime('%Y-%m-%d')
            board_number = href.split("&no=")[1].split("&divpage")[0]
            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("viewTable").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCkeck = tags.find('tbody').find_all('tr')[0].find_all('td')[1].text.strip()
            datetime.datetime.strptime(dateCkeck, "%y/%m/%d %H:%M:%S").strftime('%y/%m/%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCkeck, "%y/%m/%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            contents = tags.find('tbody').find('td', 'noborder').find('div', 'articleArea').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")

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
                'url' : href,
                'writer': writer,
                'writerIp': '',
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            if datech < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'redtea_news',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'redtea_news',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("redtea_news 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("redtea_news 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
