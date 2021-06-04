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
def saveDB(driver,date,link,writer,key):
    try:
        driver.get(link)
        driver.execute_script("document.getElementsByClassName('commentnum')[0].remove();")
        title = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME,'b')))
        content = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/table[4]/tbody/tr/td[2]/table[3]/tbody/tr/td/span'))).text.replace('\n',' ').replace("\t","")
    except TimeoutException:
        return

    paramKey = None
    if key == '공유' or key == '정유미': paramKey = key
    result = checkKeyword(title.text,content,dbKey[key]['add'],dbKey[key]['del'],paramKey)

    if result:
        conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            putKey = getPutKeyword(title.text,content,dbKey[key]['add'])
            putKeyType = getPutKeywordType(putKey,conn,curs)
            dbResult = insert(conn,'bestiz',title.text,content,writer,'',date,dbKey[key]['add'][0],putKey,putKeyType,link,link.split("&no=")[1])
        finally:
            conn.close()
    return dbResult

# 검색 소스
def startCrawling(borad,boradId):
    try:
        i = 0;check = False
        link = 'http://'+borad+'.cafe24.com/zboard/'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        for key in dbKey:
            try:
                driver.get(link+'zboard.php?id='+boradId)
                fromEle = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME,'search')))
                inputkey = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME,'keyword')))
                inputkey.send_keys(key)
                fromEle.submit()
                tbody = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'/html/body/div/table[4]/tbody/tr/td[2]/table[1]/tbody')))
            except TimeoutException:
                continue
            soup = BeautifulSoup(tbody.get_attribute("innerHTML"),'html.parser')
            trArr = soup.find_all("tr",bgcolor="white")
            for item in trArr:
                tdArr = item.find_all("td")
                url = tdArr[1].a['href']
                writer = tdArr[2].span.text
                date = datetime.datetime.strptime(tdArr[3].span['title'],'%Y년 %m월 %d일 %H시 %M분 %S초').strftime('%Y-%m-%d %H:%M:%S')
                if date < datetime.date.today().strftime('%Y-%m-%d'):
                    print(date)
                    break
                # check = saveDB(driver,date,(link+url),writer,key)
                if check: break

    finally :
        driver.quit()

if __name__=='__main__':
    start_time = time.time()

    # MySQL 연결
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # 키워드 가져오기
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("베스티즈 크롤링 시작")
    siteDic = {"besthgc":"ghm2b","bestizsky":"drb13"}
    for info in siteDic:
        startCrawling(info,siteDic[info])
    print("베스티즈 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
