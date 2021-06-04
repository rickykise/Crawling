import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import NavigableString
from bs4 import BeautifulSoup

def startCrawling(key):
    regex = re.compile(r'\d{4}-\d+-\d+ \d+:\d+:\d+')
    print("키워드 :",key)
    insertNum = 0; ninsertNum = 0;paramKey = None;check = False
    if key == '공유' or key == '정유미': paramKey = key
    link = 'http://www.ygosu.com/all_search/?type=board&add_search_log=Y&keyword='+key+'&page='

    for i in range(1,6):
        print(i,'페이지')
        r = requests.get(link+str(i))
        c = r.text
        soup = BeautifulSoup(c,'html.parser')
        liEles = soup.find("ul",id="board_search_result").find_all("li")

        for item in liEles:
            li = soup.find('li','thumbnail_body')
            if not li:
                li = soup.find('li','default_body')
            dateCheck = li.find('span','date').text
            if dateCheck < datetime.date.today().strftime('%Y-%m-%d'):
                check=True;break

            title = li.find('a','subject')
            html = requests.get(title['href']).text
            tags = BeautifulSoup(html,'html.parser')
            [s.extract() for s in tags('script')]
            body = tags.find("div",id="containerInner")
            info = tags.find('div','right_etc')
            try:
                data = {
                    'title' : title.text.strip(" "),
                    'url' : title['href'],
                    'contents' : tags.find('div','container').get_text(' ',strip=True).strip(),
                    'date': info.find('div','date').get_text(' ',strip=True).split('/')[0].replace('DATE : ','').strip(),
                    'writer': info.find('div','nickname').find('a').text.strip(),
                    'ip': tags.find('div','ipadd').get_text(' ',strip=True).replace('IP : ','').strip(),
                    'board_number':  tags.find('div','tit').find('h3').find('span').text.strip()
                }
            except:
                continue
            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            if result:
                conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'ygosu',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                finally :
                    conn.close()
        if check: break

    print("insert :",insertNum)
    print("============================")


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("와이고수 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("와이고수 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
