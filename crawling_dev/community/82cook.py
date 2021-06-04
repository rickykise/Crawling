# 82cook 검색
import openpyxl,time,pymysql,datetime
import requests
import urllib.request
from commonFun import *
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    data = {
        'contents' : (soup.find("div",id="articleBody") != None) and soup.find("div",id="articleBody").text.replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", ""),
        'date' : (soup.find("div",{"class","readRight"}) != None) and soup.find("div",{"class","readRight"}).text.replace("작성일 : ","").replace("\n","").replace("\t","").replace("\xa0", "").replace("\r", ""),
        'ip' : (soup.find("div",id="writerIP") != None) and soup.find("div",id="writerIP").text.replace("IP : ","") or '',
        'contNum' : (soup.find("div",id="contNum") != None) and soup.find("div",id="contNum").text or ''
    }
    # print(data)
    return data

def startCrawling(key):
    print("키워드 : ",key)
    encText = urllib.parse.quote(key)
    pageNum = 0;check = True;paramKey = None;insertNum = 0

    while check:
        r = requests.get("http://www.82cook.com/entiz/enti.php?bn=15&searchType=search&search1=1&keys="+encText+"&page="+str(pageNum))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tbody = soup.find("tbody")
        tr = tbody.find_all("tr")

        if len(tr) < 2:
            check = False
            print("게시물없음\n========================")
            continue

        for item in tr:
            url = "http://www.82cook.com/entiz/"+item.find("a",{"class","photolink"})['href'].replace("&page="+str(pageNum)+"&searchType=search&search1=1&keys="+encText,"")
            resultData = getContents(url)
            dateCheck = item.find("td","regdate numbers").text.find(':')
            # print(dateCheck)
            if dateCheck == -1: check=False;break

            if resultData['contNum'] is '': continue

            data = {
                'title' : item.find("td",{"class","title"}).find("a").text,
                'url' : url,
                'contents' : resultData['contents'],
                'date' : resultData['date'],
                'writer' : item.find("td",{"class","user_function"}).text,
                'ip' : (resultData['ip'] != '') and resultData['ip'].replace("IP : ","") or '',
                'board_number' : resultData['contNum']
            }
            # print(data)
            # if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            # if data['date'] < '2018-03-01': check=False;break
            if key == '공유' or key == '정유미': paramKey = key
            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

            if result:
                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                # conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'82cook',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'82cook',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
                    conn2.close()
        pageNum = pageNum + 1

        #     if item.find("a",{"class","photolink"}).text == '1':
        #         check = False
        # pageNum = pageNum + 1
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("82cook 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '흥부':
        #     startCrawling(k)
        startCrawling(k)
    print("82cook 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")