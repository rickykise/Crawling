import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def startCrawling(site):
    i = 0;check = True;
    link = 'http://theqoo.net/index.php?mid='+site+'&filter_mode=normal&page='
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    print(dbBackup)
    try:
        while check:
            i = i+1
            driver.get(link+str(i))
            textHtml = driver.find_element(By.CLASS_NAME,'bd_lst').get_attribute('innerHTML')
            soup = BeautifulSoup(textHtml,'html.parser')
            tr = soup.find('tbody').find_all("tr",class_=False)

            for item in tr:
                pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('td', 'title').find_all('a')[0].text.strip()
                timech = item.find('td', 'time').text.strip()
                hrefChek = 'http://theqoo.net' + item.find('td', 'title').find_all('a')[0]['href']
                try:
                    board_number = hrefChek.split("&document_srl=")[1]
                except:
                    pass
                href = 'http://theqoo.net/' + board_number

                timecheck = timech.find(':')
                if timecheck == -1: check=False;break
                # print(timech)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                driver.get(href)
                time.sleep(2)
                page_main = driver.find_element_by_id("content").get_attribute('innerHTML')
                tags = BeautifulSoup(page_main,'html.parser')
                dateCheck = tags.find('div', 'fr').text.strip()
                datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M").strftime('%Y.%m.%d %H:%M')
                date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')
                contents = tags.find('div', 'rd_body').find('article').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': '무명의 더쿠',
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
                    dbResult = insert(conn,site,data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,site,data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    # MySQL 연결
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # 키워드 가져오기
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("theqoo 크롤링 시작")
    site = ['square','dyb']
    for s in site:
        startCrawling(s)
    print("theqoo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
