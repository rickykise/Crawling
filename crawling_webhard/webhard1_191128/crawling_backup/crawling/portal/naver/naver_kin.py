# 네이버 검색 Open API - 지식인 검색
import datetime,pymysql,time
import requests
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getDate(url):
    date = None
    try:
        r = requests.get(url)
        c = r.text
        soup = BeautifulSoup(c,'html.parser')
        if soup.find_all("dd","date",limit=6):
            dateTags = [tag for tag in soup.find_all("dd","date",limit=6) if len(tag.contents) == 1]
            date = datetime.datetime.strptime(dateTags[0].text,'%Y.%m.%d. %H:%M').strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print('날짜크롤링에러:',e,type(e),url)

    return date

def startCrawling(key):
    apiStartNum = 1;paramKey = None;check = False;insertNum = 0
    print("키워드 : "+key)
    while apiStartNum < 1000:
        data = searchNAPI('kin',key,'100',str(apiStartNum),'date')
        if apiStartNum > data['total']: break
        for item in data['items']:
            item['title'] = setText(item['title'],0) # 제목
            item['description'] = setText(item['description'],1) # 내용
            item['link'] = item['link'].replace("?Redirect=Log&amp;logNo=","/").split('&qb=')[0] # URL
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if key == '공유' or key == '정유미': paramKey = key
            result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            date = getDate(item['link'])

            if date is None:
                continue
            elif date < '2018-02-19':
                check=True;break

            if result:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    putKeyType = (putKeyType == None) and ' ' or putKeyType
                    dbResult = insert(conn,'kintip','naver',item['title'],'',date,dbKey[key]['add'][0],putKey,putKeyType,item['link'])
                    if dbResult:
                        check=True;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
        if check: break
        apiStartNum = apiStartNum + 100
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()
    print("네이버 지식인 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] =='더보이즈':
            startCrawling(k)
        # startCrawling(k)
    print("네이버 지식인 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
