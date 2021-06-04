import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :",key)
    i = 0;
    link = 'http://issuein.org/?_filter=search&act=&vid=&mid=board&category=&search_keyword='+key+'&search_target=title'
    check = True; paramKey = None; insertNum = 0

    while check:
        textHtml = requests.get(link).text
        soup = BeautifulSoup(textHtml,'html.parser')
        if soup.find("table","bd_lst bd_tb_lst bd_tb") == None: check = False; continue
        tr = soup.find("table","bd_lst bd_tb_lst bd_tb").find("tbody").find_all("tr",class_=False)

        for item in tr:
            title = item.find("td","title").find_all('a')[0].text.replace("\n","").replace("\t","")
            dateCheck = item.find("td","time").text
            dateck = datetime.datetime.strptime(dateCheck, "%Y.%m.%d").strftime('%Y-%m-%d')
            date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d").strftime('%Y-%m-%d %H:%M:%S')
            href = 'http://issuein.com'+item.find("td","title").find('a')['href']
            html = requests.get(href).text
            tags = BeautifulSoup(html,'html.parser')
            board_number = href.split("&document_srl=")[1].split("&")[0]
            contents = tags.find('div','document_'+board_number+'_4 xe_content').text.replace("\n","").replace("\t","").replace("\xa0", "")

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
                'writer': "",
                'board_number': board_number,
                'contents' : contents,
                'date': date
            }
            # print(data)
            if dateck < datetime.date.today().strftime("%Y-%m-%d"): check=False;break

            conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'issuein',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'issuein',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    return False
            finally :
                conn.close()
                conn2.close()
        return True
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("issuein 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '블랙팬서':
        #     startCrawling(k)
        startCrawling(k)
    print("issuein 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
