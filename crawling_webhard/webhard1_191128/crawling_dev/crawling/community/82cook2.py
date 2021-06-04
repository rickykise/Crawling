# 82cook 검색
import openpyxl,time,pymysql,datetime
import requests
import urllib.request
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :", key)
    i = 0;
    link = 'http://www.82cook.com/entiz/enti.php?bn=15&searchType=search&search1=1&keys='+key+'&page='
    check = True; paramKey = None; insertNum =0

    while check:
        i = i+1
        textHtml = requests.get(link+str(i)).text
        soup = BeautifulSoup(textHtml,"html.parser")
        tbody = soup.find("tbody")
        tr = tbody.find_all("tr")

        if len(tr) < 2:
            check = False
            print("게시물없음\n========================")
            continue

        for item in tr:
            title = item.find("td",{"class","title"}).find("a")
            url = "http://www.82cook.com/entiz/"+item.find("a",{"class","photolink"})['href'].replace("&page="+str(i)+"&searchType=search&search1=1&keys="+key,"")
            contents =  (soup.find("div",id="articleBody") != None) and soup.find("div",id="articleBody").text or ''
            date = (soup.find("div",{"class","readRight"}) != None) and soup.find("div",{"class","readRight"}).text.replace("작성일 : ","").replace("\n","") or ''
            writer = item.find("td",{"class","user_function"}).text
            ip = (soup.find("div",id="writerIP") != None) and soup.find("div",id="writerIP").text.replace("IP : ","") or ''
            board_number = (soup.find("div",id="contNum") != None) and soup.find("div",id="contNum").text or ''

            result = False;addKey = None
            mkey = getMainKeyword(dbKey,title)

            if mkey:
                paramKey = None
                addKey = dbKey[mkey]['add']
                if mkey == '공유' or mkey == '정유미': paramKey = mkey
                result = checkKeyword(title,contents,dbKey[key]['add'],dbKey[key]['del'],paramKey)

            if result is False: break
            data = {
                'title' : title,
                'url' : url,
                'writer': writer,
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            print(data)
            # if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            if data['date'] < '2018-03-01': check=False;break
            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'82cook',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    check=False;break
                else:
                    insertNum = insertNum+1
            finally:
                conn.close()
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("82cook 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '흥부':
            startCrawling(k)
        # startCrawling(k)
    print("82cook 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
