import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : ",key)
    i = 0;
    link = 'http://extmovie.maxmovie.com/xe/?_filter=search&act=&vid=&mid=bestboard&category=&search_target=title&search_keyword='+key+'&page='
    check = True; paramKey = None; insertNum = 0

    while check:
        i = i+1
        textHtml = requests.get(link+str(i)).text
        soup = BeautifulSoup(textHtml,'html.parser')
        tr = soup.find("table","ldn").find("tbody").find_all("tr",class_=False)

        for item in tr:
            title = item.find("td","title").find_all('a')[0].text.replace("\n","").replace("\t","")
            if title == '신고접수로 블라인드 처리 되었습니다.': check = False; continue
            href = 'http://extmovie.maxmovie.com'+item.find("td","title").find('a')['href']
            html = requests.get(href).text
            tags = BeautifulSoup(html,'html.parser')
            board_number = href.split("&document_srl=")[1].split("&")[0]
            member_number = tags.find('header', 'atc-hd').find('ul','ldd-title-under').find_all('li')[0].find('a')['class']
            member_num = str(member_number).split("['member_")[1].split("']")[0]
            contents = tags.find('div', 'document_'+board_number+'_'+member_num+' xe_content').text.replace("\n","").replace("\t","").replace("\xa0", "")
            dateCheck = tags.find('header', 'atc-hd').find('ul', 'ldd-title-under').find('li', 'num').text.strip()
            datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')

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
                'writer': item.find('td','author').find('a').text,
                'board_number': board_number,
                'contents' : setText(contents,0),
                'date': date
            }
            if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
            # if data['date'] < '2018-02-27': check=False;break
            # print(data)
            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'extrememovie_best',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    return False
            finally :
                conn.close()
        return True
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("extrememovie_best 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '정유미':
        #     startCrawling(k)
        startCrawling(k)
    print("extrememovie_best 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
