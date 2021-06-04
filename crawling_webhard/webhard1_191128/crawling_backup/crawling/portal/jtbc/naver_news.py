# 네이버 검색 Open API - 뉴스 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from bs4 import BeautifulSoup
import datetime,time,pymysql

def startCrawling(key):
    apiStartNum = 1;paramKey = None;check=False;insertNum = 0
    if key == '공유' or key == '정유미': paramKey = key
    print("키워드 : "+key)
    while apiStartNum < 1000:
        data = searchNAPI('news',key,'100',str(apiStartNum),'date')
        if len(data['items']) == 0: break
        for item in data['items']:
            item['title'] = setText(item['title'],0) # 제목
            item['title'] = (len(item['title']) > 100) and item['title'][:96]+"…" or item['title']
            item['description'] = setText(item['description'],1) # 내용
            item['pubDate'] = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
            if item['pubDate'] < datetime.date.today().strftime('%Y-%m-%d'): continue

            result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            if result:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
                    dbResult = insert(conn,'media','naver',item['title'],item['description'],item['pubDate'],dbKey[key]['add'][0],putKey,'',item['link'])
                    if dbResult:
                        check=True;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
        if check: break
        apiStartNum = apiStartNum + 100

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 키워드 뉴스 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '손석희':
            startCrawling(k)
    print("네이버 키워드 뉴스 크롤링 끝")
    print("==============================")
    print("--- %s seconds ---" %(time.time() - start_time))
