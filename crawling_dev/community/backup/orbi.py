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
        link = "https://orbi.kr/search?q="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("panel").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        li = soup.find('ul', 'post-list').find_all('li')

        for item in li:
            pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('p', 'title').find('a').text.strip() == '회원에 의해 삭제된 글입니다.':
                continue
            title = item.find('p', 'title').find('a').text.strip()
            writer = item.find('a', 'nickname ng-isolate-scope').text.strip()
            timech = item.find('p', 'date').find('abbr').text
            href = "https://orbi.kr" + item.find('p', 'title').find('a')['href']
            board_number = href.split(".kr/")[1].split("/")[0]
            dateCkeck = item.find('p', 'date').find('abbr')['title'].split("@")[1]
            datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            contents = item.find('p', 'content').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
            if date < datetime.date.today().strftime("%Y-%m-%d"): check=False;break

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
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'orbi',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'orbi',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("orbi 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("orbi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
