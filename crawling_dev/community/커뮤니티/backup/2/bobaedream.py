# bobaedream 검색
import openpyxl,time,pymysql,datetime
import requests
import commonFun
from commonFun import *
from bs4 import BeautifulSoup

def setDate(date):
    date = date.replace(".","-")
    date = date.replace(" ","")
    date = date.replace(")"," ")
    date = date.replace(u'\xa0', u' ')
    return date

def getContents(url):
    r = requests.get(url.replace("&bm=1",""))
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    data = {}

    try:
        data['contents'] = (soup.find("div","bodyCont") != None) and soup.find("div","bodyCont").text.replace("\n","").replace(u'\xa0', u' ') or '',
        data['date'] = (soup.find("span","countGroup") != None) and setDate(soup.find("span","countGroup").text).split("|")[2].split(" ") or '',
        data['url'] = (soup.find("a","ipAdd") != None) and soup.find("a","ipAdd").text.replace(";","") or url,
        data['board_number'] = url.replace("http://www.bobaedream.co.kr//view?code=strange&No=","").split("&")[0]
        data['date'] = data['date'][0][0]+" "+data['date'][0][2]
    except:
        pass

    return data

def startCrawling(key):
    print("키워드 : ",key)
    # 보배드림 페이징 변수,insert된 게시물 변수
    pageNum = 1;insertNum = 0;ninsertNum = 0;paramKey = None;check = False
    if key == '공유' or key == '정유미': paramKey = key
    site = "http://www.bobaedream.co.kr/list?code=strange&s_cate=&maker_no=&model_no=&or_gu=10&or_se=desc&s_selday=&pagescale=10&info3=&noticeShow=&s_select=Body&s_key="+key
    # 검색된 페이지 html 가져옴
    r = requests.get(site);c = r.content;soup = BeautifulSoup(c,"html.parser")
    # 키워드 페이지 총 페이지 수 확인
    pageCheck = soup.find("ul","pageNumber03");li = pageCheck.find_all("li")
    pageCount = len(li) if len(li) < 11 else 10
    # 게시글이 없을 때
    if pageCount == 0:
        print("게시물없음\n========================")
        return

    while pageNum <= pageCount:
        r = requests.get(site+"&level_no=&vdate=&type=list&page="+str(pageNum))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tbody = soup.find("tbody")
        tr = tbody.find_all("tr",itemtype="http://schema.org/Article")

        for item in tr:
            if item.find("td","date").text.find("/") != -1:
                check=True;break
            resultData = getContents("http://www.bobaedream.co.kr/"+item.find("td",{"class","pl14"}).find("a")["href"])

            data = {
                'title' : item.find("td",{"class","pl14"}).find("a").text,
                'url' : (resultData['url'] != '') and resultData['url'][0] or '',
                'contents' : (resultData['contents'] != '') and resultData['contents'][0] or '',
                'date' : (resultData['date'] != None) and resultData['date'] or '',
                'writer' : item.find("td",{"class","author02"}).text.replace("\n",""),
                'board_number' : resultData['board_number']
            }
            if data['date'] == '': continue

            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

            if result:
                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'bobae',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
        if check: break
        pageNum = pageNum + 1
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("bobaedream 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("bobaedream 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
