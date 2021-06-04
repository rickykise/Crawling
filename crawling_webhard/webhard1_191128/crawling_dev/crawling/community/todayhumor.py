import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import NavigableString
from bs4 import BeautifulSoup

def startCrawling(key):
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    regex = re.compile(r'\d{4}-\d+-\d+ \d+:\d+:\d+')

    print("키워드 :",key)
    insertNum = 0; ninsertNum = 0;paramKey = None;check = False
    if key == '공유' or key == '정유미': paramKey = key
    link = 'http://www.todayhumor.co.kr/board/list.php?table=&kind=search&keyfield=subject&keyword='+key+'&page='

    for i in range(1,6):
        r = requests.get(link+str(i))
        c = r.text
        soup = BeautifulSoup(c,'html.parser')

        tr = soup.find("table","table_list").find("tbody").find_all("tr","view")

        if len(tr) <= 0:
            break

        for item in tr:
            html = requests.get("http://www.todayhumor.co.kr"+item.find("td","no").find("a")['href']).text
            tags = BeautifulSoup(html,'html.parser')
            body = tags.find("div",id="containerInner")
            # date, ip, board_number처리
            infoTags = [tag.string for tag in body.find("div","writerInfoContents").find_all("div") if tag.string is not None]
            ipText = [infoTags[idx] for idx,val in enumerate(infoTags) if val.find('IP') != -1].pop()
            dateText = [infoTags[idx] for idx,val in enumerate(infoTags) if val.find('등록시간') != -1].pop()
            numText = [infoTags[idx] for idx,val in enumerate(infoTags) if val.find('게시물ID') != -1].pop()
            # contents 처리
            contentsTag = BeautifulSoup(body.find("div","viewContent").get_text(), "lxml")
            contentsArr = []
            if len(contentsTag) > 0:
                contentsArr = list(contentsTag.body(string=True))

            data = {
                'title' : body.find("div","viewSubjectDiv").text.replace('\n', '').strip(" "),
                'url' : body.find("span",id="short_url_span").text,
                'contents' : ''.join((c.rstrip("\n\t")) for c in contentsArr if c != ' '),
                'date':(dateText == None) and '' or regex.search(dateText.replace("/","-")).group(),
                'writer':body.find("span",id="viewPageWriterNameSpan")['name'],
                'ip': (ipText == None) and ' ' or ipText.replace("IP : ",""),
                'board_number':re.sub('[^0-9]','',numText)
            }
            if data['date'] < datetime.datetime.now().strftime('%Y-%m-%d'): check=True;break
            data['contents'] = data['contents'].strip()
            result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

            if result:
                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'todayhumor',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'todayhumor',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                finally :
                    conn.close()
                    conn2.close()
        if check:
            break

    print("insert :",insertNum)
    print("============================")


if __name__=='__main__':
    start_time = time.time()

    # MySQL 연결
    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # 키워드 가져오기
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("오늘의 유머 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("오늘의 유머 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
