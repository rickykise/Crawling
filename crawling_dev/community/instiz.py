import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# DB 저장
def saveDB(driver,num,key):
    paramKey = None
    try:
        link = 'https://www.instiz.net/pt/'+num
        driver.get(link)
        wait = WebDriverWait(driver, 3)
        title = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="subject"]/a')))
        content = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="memo_content_1"]')))
        info = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/table/tbody/tr[1]/td/table[1]/tbody/tr[2]/td/div[1]')))
        info = info.find_elements(By.TAG_NAME,'span')
        writer = info[0].find_element(By.TAG_NAME,'a').text
        date = info[2].get_attribute('title')
    except TimeoutException:
        return

    if key == '공유' or key == '정유미': paramKey = key
    result = checkKeyword(title.text,content.text,dbKey[key]['add'],dbKey[key]['del'],paramKey)
    if result:
        conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
        conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs2 = conn2.cursor(pymysql.cursors.DictCursor)
            putKey = getPutKeyword(title.text,content.text,dbKey[key]['add'])
            putKeyType = getPutKeywordType(putKey,conn,curs)
            dbResult = insert(conn,'instiz',title.text,content.text.replace("\n"," "),writer,'',date,dbKey[key]['add'][0],putKey,putKeyType,link,num)
            insert(conn2,'instiz',title.text,content.text.replace("\n"," "),writer,'',date,dbKey[key]['add'][0],putKey,putKeyType,link,num)
            if dbResult:
                return False
        finally:
            conn.close()
            conn2.close()
    return True

# 검색 소스
def startCrawling(key):
    try:
        i = 0;check = True
        link = 'https://www.instiz.net/bbs/list.php?id=pt&stype=9&k='
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        while check:
            i = i+1
            try:
                driver.get(link+key+'&page='+str(i))
                table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'mainboard')))
            except TimeoutException:
                return

            trArr = table.find_elements(By.XPATH,'//*[@id="mainboard"]/tbody/tr')
            for item in trArr[3:]:
                num = item.find_element(By.CLASS_NAME,'listno').text
                rdate= item.find_element(By.CLASS_NAME,'regdate').text
                if rdate.find('.') != -1:
                    print(rdate)
                    check = False;break
                check = saveDB(driver,num,key)
    except Exception as e:
        print(e)
    finally :
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("인스티즈 크롤링 시작")
    for key in dbKey:
        print('키워드:',key)
        startCrawling(key)
    print("인스티즈 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
