# 네이버 검색 Open API - 블로그 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import datetime,pymysql,time

def blogCheck(link,keyword):
    result = False

    if link.find('/bboni89') != -1 and keyword == '툼레이더' or link.find('/bingo504') != -1 and keyword == '툼레이더':
        result = True

    return result

def startCrawling(key):
    yesterday = datetime.date.today() - datetime.timedelta(1)
    apiStartNum = 1;insertNum = 0;paramKey = None;dic = []
    print("키워드 : "+key)
    try:
        while apiStartNum < 1000:
            data = searchNAPI('blog',key,'100',str(apiStartNum),'date')
            if not data: break
            if apiStartNum > data['total']: break
            for item in data['items']:
                if blogCheck(item['link'],key): continue
                item['title'] = setText(item['title'],0) # 제목
                item['description'] = setText(item['description'],1) # 내용
                item['postdate'] = (item['postdate'] != '') and datetime.datetime.strptime(item['postdate'],'%Y%m%d').strftime('%Y-%m-%d') or item['postdate'] #날짜

                if item['postdate'] == '' or item['link'].find('daum') != -1: continue
                if item['postdate'] < '2019-03-13':
                    print(item['postdate'])
                    apiStartNum=1000;break
                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        item['link'] = item['link'].replace("?Redirect=Log&amp;logNo=","/")
                        item['link'] = (len(item['link']) > 255) and shortURL(item['link']) or item['link']
                        item['bloggername'] = item['bloggername'].replace('님의 블로그','').replace('님의블로그','')
                        url = checkLink(item['link']);
                        if url is False: continue
                        putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        putKeyType = (putKeyType == None) and ' ' or putKeyType
                        dbResult = insert(conn,'blog','naver',item['title'],item['bloggername'],item['postdate'],dbKey[key]['add'][0],putKey,putKeyType,item['link'])
                        insert(conn2,'blog','naver',item['title'],item['bloggername'],item['postdate'],dbKey[key]['add'][0],putKey,putKeyType,item['link'])
                        if dbResult is False:
                            insertNum = insertNum+1
                            dic.append({'keyword':putKey,'url':item['link']})
                    finally:
                        conn.close()
                        conn2.close()
            apiStartNum = apiStartNum + 100

    except:
        pass
    print("insert :",insertNum)
    print("============================")
    if dic:
        getWriter(dic,'naver','blog')

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 블로그 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '닥터프리즈너' or dbKey[k]['add'][0] == '국민여러분':
            startCrawling(k)
    print("네이버 블로그 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
