# 다음 뉴스 크롤링 - DB
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import time,datetime,pymysql

def startCrawling(key):
    searchDate = datetime.datetime.now().strftime('%Y%m%d')
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get("https://search.daum.net/search?w=news&sort=recency&q="+key+"&cluster=n&DA=PGD&s=NS&a=STCF&dc=STC&pg=1&r=1&p=1&rc=1&at=more&sd="+searchDate+"000000&ed="+searchDate+"235959&period=u")
    try:
        print("키워드 :",key)
        check=False;paramKey = None;insertNum = 0
        if key == '공유' or key == '정유미':paramKey = key

        while True:
            html = driver.find_element_by_class_name('coll_cont').get_attribute("innerHTML")
            soup = BeautifulSoup(html,"html.parser")

            findLI = soup.find_all("li")
            for item in findLI:
                info = item.find("span",{"class":"date"})
                data = {
                    'title':item.find("a",{"class":"f_link_b"}).text,
                    'contents':item.find("p",{"class":"desc"}).text,
                    'url': info.find("a") and info.find("a")['href'] or item.find("a",{"class":"f_link_b"})['href'],
                    'pubDate':datetime.datetime.strptime(searchDate,'%Y%m%d')
                }
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        dbResult = insert(conn,'media','daum',data['title'],data['contents'],data['pubDate'],dbKey[key]['add'][0],putKey,'',data['url'])
                        if dbResult:
                            check=True;break
                        else:
                            insertNum = insertNum+1
                    finally:
                        conn.close()
            if driver.find_element_by_class_name('result_message').get_attribute("class") == "result_message mg_cont hide":
                if driver.find_element_by_class_name('btn_next').get_attribute("class") != "ico_comm1 btn_page btn_next" or check:
                    break
                driver.find_element_by_class_name('btn_next').click();time.sleep(3)
            else:
                break
    except Exception as e:
        print("에러 : ",e)
    finally:
        driver.close()

    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()
    print("다음 뉴스 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '손석희':
            startCrawling(k)
    print("다음 뉴스 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
