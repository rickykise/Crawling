import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    check = False;paramKey = None;insertNum = 0
    link = 'http://mlbpark.donga.com/mp/b.php?&m=search&b=bullpen&query='+key+'&select=sct&user=&p='
    r = requests.get(link+'1')
    c = r.text
    soup = BeautifulSoup(c,'html.parser')
    numTag = soup.find("div","left_cont").find("div","page").find_all("a")
    pageNum = [num.string for num in numTag if num.string != None]

    if len(pageNum) == 0:
        runCount = 2
    else:
        runCount = int(pageNum[-1])+1

    for i in range(1,runCount):
        r = requests.get(link+str(i))
        c = r.text
        soup = BeautifulSoup(c,'html.parser')
        try:
            tr = soup.find("table","tbl_type01").find("tbody").find_all("tr")
        except:
            break
        for item in tr:
            html = requests.get(item.find("td","t_left").find("a","bullpenbox")['href']).text
            tags = BeautifulSoup(html,'html.parser')
            body = tags.find("div","left_cont")
            ulTag = body.find("ul","view_head")
            body.find("div","titles").span.decompose()
            data = {
                'title' : body.find("div","titles").text,
                'url' : "http://mlbpark.donga.com/mp/b.php?m=search&p=1&b=bullpen&id="+ulTag.find("div","text3").find("em").text,
                'contents' : remove_emoji2(body.find("div",id="contentDetail").text.replace('\xa0', '').replace('\n', '')),
                'date':ulTag.find("div","text3").find("span","val").text,
                'writer':ulTag.find("div","text_left").find("span","nick").text,
                'ip':ulTag.find("div","text4").find("em").text,
                'board_number':ulTag.find("div","text3").find("em").text[:15]
            }
            if data['date'] < datetime.datetime.now().strftime('%Y-%m-%d'): check=True;break
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
                    dbResult = insert(conn,'mlbpark',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'mlbpark',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                    else:
                        insertNum = insertNum + 1
                finally :
                    conn.close()
                    conn2.close()
        if check: break
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("mlbpark 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("mlbpark 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
