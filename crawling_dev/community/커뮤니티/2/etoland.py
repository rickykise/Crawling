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
        link = "http://www.etoland.co.kr/bbs/board.php?bo_table=star"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="mw_basic"]/table[1]/tbody/tr[2]/td/form/table/tbody/tr/td[1]/input[1]').send_keys(key)
        driver.find_element_by_xpath('//*[@id="mw_basic"]/table[1]/tbody/tr[2]/td/form/table/tbody/tr/td[1]/input[2]').click()
        time.sleep(2)
        html = driver.find_element_by_id("fboardlist").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find("tbody").find_all("tr")

        for item in tr:
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'mw_basic_list_subject') == None:
                continue
            title = item.find('td', 'mw_basic_list_subject').find_all('a')[1].text.strip()
            writer = item.find('span', 'member').text.strip()
            timech = item.find('td', 'mw_basic_list_datetime').text.strip()
            href = "http://www.etoland.co.kr" + item.find('td', 'mw_basic_list_subject').find_all('a')[1]['href'].split("..")[1]
            board_number = href.split("wr_id=")[1].split("&sca")[0]

            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_id("mw_basic").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            contents = tags.find('div',id='view_content').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
            dateyear = tags.find('span','mw_basic_view_datetime').text.strip().split(" ")[0]
            datett = tags.find('span','mw_basic_view_datetime').text.strip().split(" ")[2]
            dateCheck = dateyear + ' ' + datett
            datetime.datetime.strptime(dateCheck, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
            date = datetime.datetime.strptime(dateCheck, "%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')
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
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'etoland',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'etoland',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("etoland 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("etoland 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
