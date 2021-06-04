from commonFun import *
from bs4 import BeautifulSoup
import datetime,time,pymysql
import requests
import urllib.request

def startCrawling(key):
    print("키워드 : ",key)
    paramKey = None;check=True;i = 0;insertNum = 0
    encText = urllib.parse.quote(key)
    while check:
        i = i+1
        url = "http://www.ilbe.com/list/ilbe?page="+str(i)+"&listStyle=list&searchType=title_content&search="+encText
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        # print(soup)
        li = soup.find('ul', 'board-body').find_all('li', class_=False)

        for item in li:
            title = item.find('a', 'subject').text.strip()
            url = 'http://www.ilbe.com' + item.find('a', 'subject')['href']
            writer = item.find('span', 'global-nick nick').text.strip()
            checkDate = item.find('span', 'date').text.strip()
            if checkDate.find('-') != -1:
                break

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")

            writeDate = soup.find('span', 'date').text.strip()
            contents = soup.find('div', 'post-content').text.strip().replace('\xa0','')
            contents = setText(contents,0)

            data = {
                'title' : remove_emoji(title),
                'contents' : remove_emoji(contents),
                'date' : writeDate,
                'url' : url,
                'board_number' : '',
                'ip':'',
                'writer' : remove_emoji(writer)
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
                    dbResult = insert(conn,'ilbe',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'ilbe',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False;break
                    else:
                        insertNum = insertNum + 1
                finally:
                    conn.close()
                    conn2.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("ilbe 크롤링 시작")
    for k in dbKey.keys():
        # startCrawling(k)
        if dbKey[k]['add'][0] == '송혜교':
            startCrawling(k)
    print("ilbe 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
