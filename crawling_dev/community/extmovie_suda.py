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
        link = 'http://extmovie.maxmovie.com/xe/index.php?_filter=search&mid=movietalk&search_target=title&search_keyword='+key
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        html = driver.find_element_by_class_name("ldn").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        tr = soup.find("tbody").find_all("tr",class_=False)

        for item in tr:
            title = item.find("td","title").find_all('a')[0].text.replace("\n","").replace("\t","")
            if title == '신고접수로 블라인드 처리 되었습니다.': check = False; continue
            href = 'http://extmovie.maxmovie.com'+item.find("td","title").find('a')['href']
            driver.get(href)
            time.sleep(2)
            html = driver.find_element_by_class_name("cCon").get_attribute('innerHTML')
            tags = BeautifulSoup(html,'html.parser')

            board_number = href.split("&document_srl=")[1].split("&")[0]
            member_number = tags.find('header', 'atc-hd').find('ul','ldd-title-under').find_all('li')[0].find('a')['class']
            member_num = str(member_number).split("['member_")[1].split("']")[0]
            contents = tags.find('div', 'document_'+board_number+'_'+member_num+' xe_content').text.replace("\n","").replace("\t","").replace("\xa0", "")
            dateCheck = tags.find('header', 'atc-hd').find('ul', 'ldd-title-under').find('li', 'num').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')

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
                'writer': item.find('td','author').find('a').text,
                'board_number': board_number,
                'contents' : setText(contents,0),
                'date': date
            }
            if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            # if data['date'] < '2019-01-12': check=False;break
            # print(data)

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'extrememovie',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'extrememovie',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
            finally :
                conn.close()
                conn2.close()
        return True

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

    print("extmovie_suda 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("extmovie_suda 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
