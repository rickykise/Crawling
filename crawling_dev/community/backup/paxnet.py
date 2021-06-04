import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div', 'board-view')

    dateCkeck = div.find('p', 'text').find('span', 'time')['data-date-format'].split(".")[0]
    datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
    contents = div.find('div', 'board-view-cont').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")

    data = {
        'contents': contents,
        'date': date
    }
    # print(data)
    return data

def startCrawling(key):
    print("키워드 : ",key)
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        i = 0;
        link = "http://paxnet.moneta.co.kr/tbbs/list?tbbsType=S&id=N10991&page=1&sType=cnt&sText="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("board-type").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        li = soup.find('ul', 'comm-list opt-list').find_all('li',class_=False)

        for item in li:
            pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = item.find('div', 'title').find('a').text.strip()
            writer = item.find('div', 'write').find('a').text.strip()
            timech = item.find('div', 'date').text.strip()
            board_number = item.find('div', 'title').find('a')['href'].split("(")[1].split(")")[0]
            href = "http://paxnet.moneta.co.kr/tbbs/view?tbbsType=S&id=N10991&seq="+board_number+"&sType=cnt&sText="+key
            resultData = getContents(href)

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

            if result is False: continue

            data = {
                'title' : title,
                'url' : href,
                'writer': writer,
                'writerIp': '',
                'board_number': board_number,
                'contents' : resultData['contents'],
                'date': resultData['date'],
            }
            # print(data)

            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'paxnet',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'paxnet',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("paxnet 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("paxnet 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
