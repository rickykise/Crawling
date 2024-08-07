# 다음 검색 Open API - 블로그 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import datetime,pymysql,time

def startCrawling(key):
    apiStartNum = 1;insertNum = 0;ninsertNum = 0;paramKey = None;dic = []
    if key == '공유' or key == '정유미': paramKey = key
    print("키워드 : "+key)
    while True:
        data = searchDAPI('blog',key,str(apiStartNum))
        for item in data['documents']:
            item['datetime'] = datetime.datetime.strptime(item['datetime'], '%Y-%m-%dT%H:%M:%S.000+09:00')
            if item['url'].find('naver') != -1 or item['datetime'].strftime('%Y-%m-%d') < datetime.datetime.now().strftime('%Y-%m-%d'):
                continue

            item['title'] = setText(item['title'],0) # 제목
            item['contents'] = setText(item['contents'],1) # 내용
            result = checkKeyword(item['title'],item['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

            if result:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    putKey = getPutKeyword(item['title'],item['contents'],dbKey[key]['add'])
                    dbResult = insert(conn,'blog','daum',item['title'],item['blogname'],item['datetime'],dbKey[key]['add'][0],putKey,'',item['url'])

                    if dbResult is False:
                        insertNum = insertNum+1
                        dic.append({'keyword':putKey,'url':item['url']})
                finally:
                    conn.close()
        if  data["meta"]["is_end"] == False:
            apiStartNum = apiStartNum + 1
        else:
            break
    print("insert :",insertNum)
    print("ninsert :",ninsertNum)
    print("============================")
    if dic:
        getWriter(dic,'daum','blog')


if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs) # 키워드 가져오기
    conn.close()
    print("다음 블로그 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '손석희':
            startCrawling(k)
    print("다음 블로그 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
