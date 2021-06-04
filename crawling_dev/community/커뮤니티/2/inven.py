import requests
import pymysql,time,datetime
from commonFun import *
from bs4 import NavigableString
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :",key)
    insertNum = 0;paramKey = None;check = False

    try:
        link = 'http://www.inven.co.kr/board/powerbbs.php?name=subjcont&keyword='+key+'&x=0&y=0&come_idx=2097&iskin=&mskin=&query=list&my=&category=&sort=PID&orderby=&sterm=&p='

        for i in range(1,6):
            r = requests.get(link+str(i))
            c = r.text
            soup = BeautifulSoup(c,'html.parser')
            tr = soup.find("form",{"name":"board_list1"}).find("table").find("tbody").find_all("tr","tr")

            if len(tr) <= 0: break

            for item in tr:
                titleEle = item.find("td","bbsSubject")
                if item.find("td","date").text.find('-') != -1: check=True;break

                html = requests.get(titleEle.find("a")['href']).text
                tags = BeautifulSoup(html,'html.parser')
                [s.extract() for s in tags('script')]
                body = tags.find("div","articleView")
                data = {
                    'title' : body.find("div","articleTitle").find('h1').text.strip(),
                    'url' : body.find("a",id="viewUrl")['href'],
                    'contents' : body.find('div','contentBody').get_text(' ',strip=True).strip(),
                    'date': body.find("div","articleDate").text.strip(),
                    'writer': body.find("div","articleWriter").find("span").get_text('',strip=True).strip(),
                    'ip': '',
                    'board_number': titleEle.find("span","sj_cm")['data-cmt-uid']
                }

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'inven',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        insert(conn2,'inven',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check=True;break
                        else:
                            insertNum = insertNum + 1
                    finally :
                        conn.close()
                        conn2.close()
            if check: break
    except:
        pass
    print("insert :",insertNum)
    print("============================")


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("인벤 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("인벤 유머 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
