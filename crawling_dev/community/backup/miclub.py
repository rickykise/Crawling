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
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        i = 0;
        link = "http://micon.miclub.com/board/listArticle.do?cateNo=122&reCateNo=60&searchType=1&searchText="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("tb_list").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find("tbody").find_all("tr")

        for item in tr:
            conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'view') == None:
                continue
            title = item.find('div', 'view_sbj ').find('a').text.strip()
            writer = item.find('td', ' writer').text.strip()
            timech = item.find('td', ' date').text.strip()
            href = "http://micon.miclub.com"+item.find('div', 'view_sbj ').find('a')['href']
            board_number = href.split("?artiNo=")[1].split("&hit")[0]

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("board").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCheck = tags.find('div','info01').find('span', 'date').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            contents = tags.find('div', 'viewContentArea').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
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
            print(data)

            conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'miclub',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    check=False
            finally :
                conn.close()
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("miclub 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("miclub 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
