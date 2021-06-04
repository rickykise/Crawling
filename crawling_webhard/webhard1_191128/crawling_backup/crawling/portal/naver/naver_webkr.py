# 네이버 검색 Open API - 블로그 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import datetime,pymysql,time

def startCrawling(key):
    yesterday = datetime.date.today() - datetime.timedelta(1)
    apiStartNum = 1;insertNum = 0;paramKey = None;dic = []
    print("키워드 : "+key)
    try:
        while apiStartNum < 1000:
            data = searchNAPI('webkr',key,'100',str(apiStartNum),'webkr')
            for item in data['items']:
                item['title'] = setText(item['title'],0) # 제목
                item['description'] = setText(item['description'],1) # 내용
                item['lastBuildDate'] = (item['lastBuildDate'] != '') and datetime.datetime.strptime(item['lastBuildDate'],'%Y%m%d').strftime('%Y-%m-%d') or item['lastBuildDate'] #날짜
                print(item['lastBuildDate'])
                # print(item['title'])
                # item['postdate'] = (item['postdate'] != '') and datetime.datetime.strptime(item['postdate'],'%Y%m%d').strftime('%Y-%m-%d') or item['postdate'] #날짜

    except Exception as e:
        print("Error Code:",e)
    # print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 웹문서 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("네이버 웹문서 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
