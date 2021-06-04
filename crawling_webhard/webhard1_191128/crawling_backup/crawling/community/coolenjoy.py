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
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        i = 0;
        link = "http://www.coolenjoy.net/bbs/freeboard2?bo_table=freeboard2&sca=&sop=and&sfl=wr_subject&stx="+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_id("fboardlist").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find("tbody").find_all("tr")

        for item in tr:
            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'td_num').text.strip() == '인사' or item.find('td', 'td_num').text.strip() == '공지':
                continue
            title = item.find('td', 'td_subject').find('a').text.split("댓글")[0].strip()
            writer = item.find('td', 'td_name sv_use').text.strip()
            timech = item.find('td', 'td_date').text.strip()
            href = item.find('td', 'td_subject').find('a')['href']
            board_number = href.split("freeboard2/")[1].split("?sfl")[0]

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_id("container2").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCkeck = tags.find('section',id='bo_v_info').find_all('strong')[1].text
            datetime.datetime.strptime(dateCkeck, "%y-%m-%d %H:%M").strftime('%y-%m-%d %H:%M')
            date = datetime.datetime.strptime(dateCkeck, "%y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')
            contents = tags.find('div', id='bo_v_con').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
            timecheck = timech.find(':')
            # if timecheck == -1: check=False;break
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
                'contents' : contents,
                'date': date
            }
            print(data)

            # conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            # conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            # try:
            #     curs = conn.cursor(pymysql.cursors.DictCursor)
            #     curs2 = conn2.cursor(pymysql.cursors.DictCursor)
            #     putKey = getPutKeyword(data['title'],data['contents'],addKey)
            #     putKeyType = getPutKeywordType(putKey,conn,curs)
            #     dbResult = insert(conn,'coolenjoy',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
            #     insert(conn2,'coolenjoy',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("coolenjoy 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("coolenjoy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
