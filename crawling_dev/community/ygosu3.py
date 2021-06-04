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
        link = "https://www.ygosu.com/community/all_article/?search="+key+"&searcht=s&order=&newwindow=&split_idx=0&page="
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("board_wrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table', 'bd_list')
        tr = table.find('tbody').find_all('tr')

        for item in tr:
            pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = item.find('td', 'tit').find('a').text.strip().split("(")[0]
            writer = item.find('td', 'name').find('a').text.strip()
            timech = item.find('td', 'date').text.strip()
            href = 'https://www.ygosu.com' + item.find('td', 'tit').find('a')['href']
            board_number = href.split("&rno=")[1].split("&page=")[0]
            timecheck = timech.find(':')
            if timecheck == -1: check=False;break
            print(timech)

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("board_body").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCkeck = tags.find('div', 'date').text.strip().split("DATE : ")[1].split(" / READ")[0]
            datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCkeck, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            contents = tags.find('div', 'container').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").split("var editor")[0]
            writerIp = tags.find('div', 'ipadd').text.strip().split("IP : ")[1]


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
                'writerIp': writerIp,
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
                dbResult = insert(conn,'ygosu',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'ygosu',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("ygosu 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("ygosu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
