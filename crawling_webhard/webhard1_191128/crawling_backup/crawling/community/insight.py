import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :",key)
    i = 0;
    link = "https://www.insight.co.kr/search/?page="
    link2 = "&query="+key+"&seoType=all&seoArea=all&seoDate=all&seoSort=dd"
    check = True; paramKey = None; insertNum = 0

    while check:
        i = i+1
        textHtml = requests.get(link+str(i)+link2).text
        soup = BeautifulSoup(textHtml, 'html.parser')
        if soup.find('div', 'search-result'):
            break
        div = soup.find('div', 'search-list')
        li = div.find('ul').find_all('li',class_=False)

        for item in li:
            title = item.find('a', 'search-list-article-title').text
            href = item.find('a', 'search-list-article-title')['href']
            writer = item.find('span','search-list-article-byline').text.strip().split("기자")[0]+'기자'
            if item.find('span','search-list-article-byline').text.find('기자') == -1:
                date = item.find('span','search-list-article-byline').text.strip()
            elif item.find('span','search-list-article-byline').text.find('기자') != -1:
                date = item.find('span','search-list-article-byline').text.strip().split("· ")[1]
            board_number = href.split("news/")[1]
            contents = item.find('span','search-list-article-summary').text.replace("\n","").replace("\t","").replace("\xa0", "")

            data = {
                'title' : title,
                'url' : href,
                'writer': writer,
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            # print(data)
            if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break

            result = False;addKey = None
            mkey = getMainKeyword(dbKey,title)

            if mkey:
                paramKey = None
                addKey = dbKey[mkey]['add']
                if mkey == '공유' or mkey == '정유미': paramKey = mkey
                result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

            if result is False: continue

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'insight',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'insight',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    return False
            finally :
                conn.close()
                conn2.close()
        return True

    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("insight크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("insight크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
