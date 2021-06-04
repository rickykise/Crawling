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
        link = "http://bbs.ruliweb.com/community/board/300143/list?search_type=subject&search_key="+key+"&page="
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("subtop_center_w").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find('table', 'board_list_table').find("tbody").find_all("tr",class_='table_body')

        for item in tr:
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'divsn').text.strip() == '전체공지':
                continue
            if item.find('td', 'divsn').text.strip() == '공지':
                continue
            if item.find('td', 'divsn').text.strip() == '결과값이 없습니다.':
                break
            title = item.find('td', 'subject').find('a').text.strip()
            writer = item.find('td', 'writer text_over').find('a').text
            timech = item.find('td', 'time').text.strip()
            href = item.find('td', 'subject').find('a')['href'].split("?search")[0]
            board_number = href.split("read/")[1]
            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_class_name("board_main").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            contents = tags.find('div', 'view_content').text.replace("\n","").replace("\t","").replace("\xa0", "")
            dateCheck = tags.find('div', 'col user_info_wrapper').find('span', 'regdate').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y.%m.%d (%H:%M:%S)").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d (%H:%M:%S)").strftime('%Y-%m-%d %H:%M:%S')
            writerip = tags.find('div', 'col user_info_wrapper').find('div', 'user_info').find_all('p')[5].find_all('span')[2].text.split("IP :")[1].strip()
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
                'writerIp': writerip,
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'ruliweb',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("ruliweb 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '곤지암':
        #     startCrawling(k)
        startCrawling(k)
    print("ruliweb 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
