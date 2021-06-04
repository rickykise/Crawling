import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def startCrawling(site):
    i = 0;check = True
    link = 'http://theqoo.net/index.php?mid='+site+'&filter_mode=normal&page='
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            i = i+1
            driver.get(link+str(i))
            textHtml = driver.find_element(By.CLASS_NAME,'hide_notice').get_attribute('innerHTML')
            soup = BeautifulSoup(textHtml,'html.parser')
            tr = soup.find_all("tr",class_=False)

            for item in tr:
                title = item.find("td","title").find("span").text
                dateCheck = item.find("td","time").text.strip()

                if dateCheck.find(".") != -1:
                    check = False;break

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                driver.get('http://theqoo.net/'+item.find("td","title").find("a")['href'])
                html = driver.find_element(By.CLASS_NAME,'bd_load_target').get_attribute('innerHTML')
                tags = BeautifulSoup(html,'html.parser')
                body = tags.find("div","rd_body").find("div").get_text("",strip=True).strip()
                href = tags.find("a","link")['href']
                data = {
                    'title' : tags.find("div","top_area").find("h1").find('span').text.strip(),
                    'url' : href,
                    'contents' : body,
                    'date': tags.find("span","date").text.strip(),
                    'board_number': re.sub('[^0-9]', '', href)
                }

                conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,site,data['title'],data['contents'],'무명의 더쿠','',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check = False;break
                finally :
                    conn.close()
    except Exception as e:
        print("Error Code:",e)
    finally:
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    # MySQL 연결
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # 키워드 가져오기
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("theqoo 크롤링 시작")
    site = ['square','dyb']
    for s in site:
        startCrawling(s)
    print("theqoo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
