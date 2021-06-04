import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    dateCkeck = soup.find('div', 'b_txt').find('span').text.strip()
    date = datetime.datetime.strptime(dateCkeck, "%Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
    contents_a = soup.find('div', 'news_con').find('pre').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").split(" […]")[0]
    contents = setText(contents_a,0)

    data = {
        'contents': contents,
        'date': date
    }
    # print(data)
    return data

def startCrawling(key):
    key = key.replace(" ","")
    print("키워드 :",key)
    link = "http://postshare.co.kr/?s="+key
    check = True; paramKey = None; insertNum = 0
    try:
        while check:
            textHtml = requests.get(link).text
            soup = BeautifulSoup(textHtml, 'html.parser')
            div = soup.find('div', 'list')
            li = div.find('ul').find_all('li',class_=False)

            for item in li:
                title = item.find('div', 'r_con').find('a').text.strip()
                href = item.find('div', 'r_con').find('a')['href']
                board_number = href.split("archives/")[1]
                writer = item.find('div', 'b_info').find_all('span')[1].text.strip().split(" /")[0]
                resultData = getContents(href)

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': writer,
                    'board_number': board_number,
                    'contents' : resultData['contents'],
                    'date': resultData['date'],
                }
                if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
                # if data['date'] < '2018-06-21': check=False;break
                # print(data)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'postshare',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insertNum = insertNum +1
                    if dbResult:
                        return False
                finally :
                    conn.close()
            return True
    finally:
        print("insertNum : " + str(insertNum))
        print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("postshare크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("postshare크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
