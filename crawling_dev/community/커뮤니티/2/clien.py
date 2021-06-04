import openpyxl,time,pymysql,datetime
import requests
import urllib.request
from commonFun import *
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    data = None
    try:
        data = {
            'title' : soup.find('h3','post_subject').find('span',class_=False).get_text(' ',strip=True).strip(),
            'writer' : soup.find('span','nickname').get_text(' ',strip=True).strip(),
            'contents': soup.find('div','post_content').find('article').get_text(' ',strip=True).strip(),
            'date' : soup.find('div','post_author').find_all('span',class_=False)[0].text.strip().replace("\n","").replace("\t","").split(" 수정일")[0],
            'ip' : soup.find('div','post_author').find_all('span',class_=False)[1].text.strip().replace("♡", "x"),
            'board_number' : soup.find('input',id='boardSn')['value'],
            'url' : soup.find('link',{'rel':'canonical'})['href']
        }
        if data['ip'] == '' or data['ip'] == None:
            data['ip'] = ''
        if data['writer'] == '':
            data['writer'] = soup.find('span','nickname').find('img')['alt']
    except:
        pass
    return data

def startCrawling(key):
    print("키워드 : ",key)
    encText = urllib.parse.quote(key)
    pageNum = 0;check = True;paramKey = None;insertNum = 0

    while check:
        r = requests.get("https://www.clien.net/service/search?sort=recency&boardCd=&isBoard=false&q="+encText+"&p="+str(pageNum))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        slist = soup.find("div","search_list")
        ele = slist.find_all("div","list_item")

        if len(ele) < 2:
            check = False
            print("게시물없음\n========================")
            continue

        for item in ele:
            date = item.find('div','list_time').find('span','time').text
            if date < datetime.date.today().strftime('%Y-%m-%d'):
                check=False;break

            data = getContents(item.find('a','list_subject')['href'])
            if not data: continue
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
                    dbResult = insert(conn,'clien',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'clien',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
                    conn2.close()
        pageNum = pageNum + 1
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("clien 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("clien 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
