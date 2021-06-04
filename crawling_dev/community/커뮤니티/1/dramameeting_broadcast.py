import requests,re
import pymysql,time,datetime
from commonFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 :",key)
    i = 0;
    link = "http://www.dramameeting.com/?_filter=search&act=&vid=&mid=broadcast&category=&search_keyword="+key+"&search_target=title_content&page="
    check = True; paramKey = None; insertNum = 0
    try:
        while check:
            i = i+1
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            tr = soup.find("table", "bd_lst bd_tb_lst bd_tb").find("tbody").find_all("tr",class_=False)

            for item in tr:
                title = item.find("td","title").find_all('a')[0].text.replace("\n","").replace("\t","").strip()
                hrefCheck = item.find("td","title").find('a')['href']
                href = 'http://www.dramameeting.com'+hrefCheck
                board_number = href.split("&document_srl=")[1]

                r = requests.get(href)
                c = r.content
                tags = BeautifulSoup(c,"html.parser")
                dateCheck = tags.find("span", "date m_no").text.strip()
                date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')
                contents = tags.find('div','rd rd_nav_style2 clear').find('div','xe_content').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
                # contents = tags.find('div','document_'+board_number+'_0 xe_content').text.replace("\n","").replace("\t","").replace("\xa0", "")
                # writer = item.find("td","author").text
                # print(board_number)

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': '',
                    'board_number': board_number,
                    'contents' : setText(contents,0),
                    'date': date
                }
                # print(data)
                if data['date'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
                # if data['date'] < '2018-04-08': check=False;break

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                # if mkey:
                #     paramKey = None
                #     addKey = dbKey[mkey]['add']
                #     if mkey == '공유' or mkey == '정유미': paramKey = mkey
                #     result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)
                #
                # if result is False: break

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(data['title'],data['contents'],addKey)
                putKeyType = getPutKeywordType(putKey,conn,curs)
                dbResult = insert(conn,'dramameeting_broad',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                insert(conn2,'dramameeting_broad',data['title'],data['contents'],data['writer'],'',data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                if dbResult:
                    return False
            finally :
                conn.close()
                conn2.close()
            return True
    except:
        pass
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("dramameeting broadcast크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '아이유':
        #     startCrawling(k)
        startCrawling(k)
    print("dramameeting broadcast크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
