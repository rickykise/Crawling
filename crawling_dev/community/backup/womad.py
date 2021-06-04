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
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(url)
        time.sleep(10)
        page_main = driver.find_element_by_class_name("textsize-normal").get_attribute('innerHTML')
        tags = BeautifulSoup(page_main,'html.parser')

        title = tags.find('div', 'divleft').find('b').text.strip()
        writer = tags.find('div', 'divclear').find('b').text.strip()
        date = tags.find('div', 'divright').text.strip()
        contentsCh = tags.find('div', 'content').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
        contents = setText(contentsCh,0)

        data = {
            'title' : title,
            'url' : url,
            'writer': writer,
            'contents' : contents,
            'date': date
        }
        print(data)

    finally:
        driver.close()

    return data

def startCrawling(key):
    i = 0;check = True
    print("키워드 : ",key)
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    while check:
        try:
            i = i+1
            link = "https://womad.life/s/"+key+"/"
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i))
            time.sleep(10)
            html = driver.find_element_by_class_name("basic").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")
            if len(tr) < 2:
                check = False
                print("게시물없음\n========================")
                break

            for item in tr:
                conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                dateCkeck = item.find_all('td')[3].text.strip()
                if dateCkeck.find(':') == -1: check=False;break
                url = 'https://womad.life' + item.find('td', 'text-left').find('a')['href']
                board_number = item.find('td', 'text-left').find('a')['href'].split("/")[1]
                resultData = getContents(url)

                data = {
                    'title' : resultData['title'],
                    'url' : url,
                    'writer': resultData['writer'],
                    'writerIp': '',
                    'board_number': board_number,
                    'contents' : resultData['contents'],
                    'date': resultData['date'],
                }
                # print(data)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,data['title'])

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(data['title'],None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: break

                # conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                # conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
                # try:
                #     curs = conn.cursor(pymysql.cursors.DictCursor)
                #     curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                #     putKey = getPutKeyword(data['title'],data['contents'],addKey)
                #     putKeyType = getPutKeywordType(putKey,conn,curs)
                #     dbResult = insert(conn,'womad',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                #     insert(conn2,'womad',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                #     if dbResult:
                #         check=False
                # finally :
                #     conn.close()
                #     conn2.close()
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

    print("womad 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '유아인':
        #     startCrawling(k)
        startCrawling(k)
    print("womad 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
