from commonFun import *
from bs4 import BeautifulSoup
import datetime,time,pymysql
import requests
import urllib.request

def getContents(link):
    data = None
    try:
        html = requests.get(link).content
        eles = BeautifulSoup(html,"html.parser")
        header = eles.find("div","readHeader")
        del eles.find("div",id="copy_layer_1").contents[-1]
        data = {
            'title' : remove_emoji(header.h1.a.text),
            'contents' : remove_emoji(eles.find("div",id="copy_layer_1").get_text(" ", strip=True).strip().replace('\xa0','')),
            'date' : header.find("div","date").get_text().strip(),
            'url' : header.find("div","uri").a['href'],
            'board_number' : '',
            'ip':'',
            'writer' : remove_emoji(header.find("div","author").get_text(" ", strip=True))
        }
        data['board_number'] = data['url'].split("com/")[1]
        if data['date'].find("(") != -1:
            dateArr = data['date'].split("(")
            data['date'] = dateArr[0]
            data['ip'] = dateArr[1].replace(")","")
    except Exception as e:
        print(e,link)
    return data

def startCrawling(key):
    print("키워드 : ",key)
    paramKey = None;check=True;i = 0;insertNum = 0
    encText = urllib.parse.quote(key)
    while check:
        url = "http://www.ilbe.com/index.php?act=IS&where=document&is_keyword="+encText+"&mid=index&search_target=title_content&page="
        i = i+1
        r = requests.get(url+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        try:
            liList = soup.find("ul","searchResult").find_all("li")
        except:
            break
        for item in liList:
            # 게시물이 오늘 날짜인지 확인 및 게시물이 존재하는 게시물인지 확인
            timeCheck = item.find("span","time").text.split(" ")[0]
            pUrl = item.find("dt").find("a")["href"]
            if timeCheck < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            if pUrl == 'http://www.ilbe.com/': continue
            # 게시물의 내용이 제대로 들어왔는지 확인
            data = getContents(pUrl)
            if not data: continue
            # DB에 넣을 게시물인지 확인
            if key == '공유' or key == '정유미': paramKey = key
            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            if result:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'ilbe',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False;break
                    else:
                        insertNum = insertNum + 1
                finally:
                    conn.close()
    print("insert:",insertNum)
    print("==========================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("ilbe 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("ilbe 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
