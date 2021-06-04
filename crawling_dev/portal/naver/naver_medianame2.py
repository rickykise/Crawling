import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *

#url 가져오기
def getUrlCheck(url,conn,curs):
    print(url)
    with conn.cursor() as curs:
        sql = 'SELECT url FROM media_data where media_check = 0 and url = %s;'
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                return b
        else:
            a == None
            return a

def startCrawling(key):
    print("키워드 : ",key)
    updateNum = 0;start = 1;i = 0;paramKey = None
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    searchDay = datetime.datetime.now()
    searchDate = searchDay.strftime('%Y.%m.%d')
    searchDate2 = searchDay.strftime('%Y%m%d')
    link = "https://search.naver.com/search.naver?&where=news&query="+key+"&sm=tab_pge&sort=1&photo=0&field=0&reporter_article=&pd=3&ds="+searchDate+"&de="+searchDate+"&docid=&nso=so:dd,p:from"+searchDate2+"to"+searchDate2+",a:all&mynews=0&start="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        driver.get(link+str(start));time.sleep(3)
        try:
            total = int(driver.find_element_by_class_name('title_desc').text.split(" / ")[1].replace(",","").replace("건",""))
        except:
            return
        if total > 600: total = 600
        while start < total:
            html = driver.find_element_by_class_name('main_pack').find_element_by_class_name("type01").get_attribute('innerHTML')
            soup = BeautifulSoup(html,"html.parser")
            findLI = soup.find_all("li")
            for item in findLI:
                media_name = item.find('span', '_sp_each_source').text.strip()
                url = item.find('a', '_sp_each_url')['href'].replace(" ","")
                checkUrl = getUrlCheck(url,conn,curs)
                # print(checkUrl)
                if checkUrl != None:
                    try:
                        sql = "update media_data set media_name=%s, media_check=1 where url=%s and media_name = 'naver';"
                        curs.execute(sql, (media_name, checkUrl))
                        conn.commit()
                        updateNum = updateNum+1
                        i = i+1
                    except Exception as e:
                        if e.args[0] == 1062:
                            sql = "delete from media_data where media_name = 'naver' and url =%s;"
                            curs.execute(sql, (checkUrl))
                            conn.commit()
                            continue
                elif checkUrl == None:
                    continue

            start = start+10
            driver.get(link+str(start));
            time.sleep(5)
    # except:
    #     pass
    finally:
        driver.close()
    print("updateNum :",updateNum)
    print("=============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("naver_medianame 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("naver_medianame 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
