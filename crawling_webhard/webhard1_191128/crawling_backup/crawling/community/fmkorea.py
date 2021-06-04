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
        link = "https://www.fmkorea.com/?vid=&mid=humor&category=&search_keyword="+key+"&search_target=title"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("bd_lst_wrp").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        table = soup.find('table', 'bd_lst bd_tb_lst bd_tb')
        tr = table.find('tbody').find_all('tr')

        for item in tr:
            pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('td', 'cate').text == '공지' or item.find('td', 'cate').text == '유머':
                continue
            title = item.find('td', 'title').find_all('a')[0].text.strip()
            writer = item.find('td', 'author').find('a').text.strip()
            timech = item.find('td', 'time').text.strip()
            href = 'https://www.fmkorea.com' + item.find('td', 'title').find_all('a')[0]['href']
            board_number = href.split("&document_srl=")[1].split("&search_keyword")[0]
            driver.get(href)
            time.sleep(2)
            page_main = driver.find_element_by_id("content").get_attribute('innerHTML')
            tags = BeautifulSoup(page_main,'html.parser')
            dateCkeck = tags.find('div', 'top_area ngeb').find('span').text
            datetime.datetime.strptime(dateCkeck, "%Y.%m.%d %H:%M").strftime('%Y.%m.%d %H:%M')
            date = datetime.datetime.strptime(dateCkeck, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')
            contentsch = tags.find('div', 'rd_body clear').find('article').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
            if contentsch.find('Video 태그') != -1:
                contents = ''
            elif contentsch.find('Video 태그') == -1:
                contents = contentsch
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
                'contents' : setText(contents,0),
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
                dbResult = insert(conn,'fmkorea',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'fmkorea',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

    print("fmkorea 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("fmkorea 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
