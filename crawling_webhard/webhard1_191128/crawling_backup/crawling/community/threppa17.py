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
        link = "https://threppa.com/bbs/board.php?bo_table=0205&sca=&sfl=wr_subject%7C%7Cwr_content&stx="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("list-tbl").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find("tbody").find_all("tr")

        for item in tr:
            conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if len(item) < 2:
                check = False
                print("게시물없음\n========================")
                break
            title = item.find('td', 'list-subject').find('a').text.strip()
            writer = item.find('td', 'list-name').find('span').text.strip()
            timecheck = item.find('td', 'list-date list-date3').text.strip()
            timech = '2018-'+item.find('td', 'list-date list-date3').text.strip()
            datetime.datetime.strptime(timech, "%Y-%m.%d").strftime('%Y-%m.%d')
            date = datetime.datetime.strptime(timech, "%Y-%m.%d").strftime('%Y-%m-%d %H:%M:%S')
            href = item.find('td', 'list-subject').find('a')['href']
            board_number = href.split("&wr_id=")[1].split("&sfl=")[0]
            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("viewContents").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            contents = tags.text.strip().replace("\n","").replace("\t","").replace("\xa0", "").split("- 쓰레빠닷컴")[0]
            print(timecheck)
            if timecheck < datetime.date.today().strftime("%m-%d"): check=False;break
            # if timech2 < '03-16': check=False;break

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

            conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'threppa',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    check=False
            finally :
                conn.close()
    # except:
    #     pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("threppa 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("threppa 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
