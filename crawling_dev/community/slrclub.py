# slrclub 검색
import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ", key)
    link = 'http://www.slrclub.com/bbs/zboard.php?id=free&page='
    check = True; paramKey = None; insertNum =0
    # 검색된 페이지 html 가져옴
    r = requests.get(link);c = r.content;soup = BeautifulSoup(c,"html.parser")
    # 키워드 페이지 총 페이지 수 확인
    pageCheck = soup.find("table","pageN")
    page = pageCheck.find_all('a')[9].text
    pageNum = int(''.join(list(filter(str.isdigit,page))))

    while check:
        textHtml = requests.get(link+str(pageNum)).text
        print(link+str(pageNum))
        soup = BeautifulSoup(textHtml,'html.parser')
        tr = soup.find("table","bbs_tbl_layout").find("tbody").find_all("tr",class_=False)

        for item in tr:
            if item.find('td', 'list_notice'):
                continue
            if item.find('td', 'sbj').text == '삭제된 게시물입니다. ': check=False;continue
            title = item.find('td', 'sbj').find('a').text
            time = item.find('td', 'list_date no_att').text
            href = 'http://www.slrclub.com' + item.find('td', 'sbj').find('a')['href']
            writer = item.find('td', 'list_name').text
            html = requests.get(href).text
            tags = BeautifulSoup(html,'html.parser')
            board_number = href.split("&no=")[1]
            content = tags.find('div', id="userct").text.replace("\n","").replace("\t","")
            dateCheck = tags.find('td', 'date bbs_ct_small').find('span').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y/%m/%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            date = datetime.datetime.strptime(dateCheck, "%Y/%m/%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            timecheck = time.find(':')
            if timecheck == -1: check=False;break
            # print(time)

            result = False;addKey = None
            mkey = getMainKeyword(dbKey,title)

            if mkey:
                paramKey = None
                addKey = dbKey[mkey]['add']
                if mkey == '공유' or mkey == '정유미': paramKey = mkey
                result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

            if result is False: break
            data = {
                'title' : title,
                'url' : href,
                'writer': writer,
                'board_number': board_number,
                'contents' : content,
                'date': date
            }
            # print(data)
            
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'slrclub',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'slrclub',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    check=False
            finally :
                conn.close()
                conn2.close()

        pageNum = pageNum - 1
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("slrclub 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '정유미':
        #     startCrawling(k)
        startCrawling(k)
    print("slrclub 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
