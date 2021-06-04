# 다음 검색 Open API - web 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import datetime,pymysql,time

def startCrawling(key):
    apiStartNum = 1;insertNum = 0;paramKey = None
    try:
        while True:
            data = searchDAPI('web',key,str(apiStartNum))
            for item in data['documents']:
                item['datetime'] = datetime.datetime.strptime(item['datetime'], '%Y-%m-%dT%H:%M:%S.000+09:00').strftime('%Y-%m-%d %H:%M:%S')
                if item['datetime'] < '2019-03-13': data["meta"]["is_end"] = True;break
                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(item['title'],item['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if not result: continue
                url = checkLink(item['url']);
                if url is False: continue
                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                conn2 = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    item['title'] = setText(item['title'],0) # 제목
                    item['contents'] = setText(item['contents'],1) # 내용
                    item['title'] = (len(item['title']) > 50) and item['title'][:47]+"…" or item['title']
                    putKey = getPutKeyword(item['title'],item['contents'],dbKey[key]['add'])
                    dbResult = insert(conn,'webdoc','daum',item['title'],'',item['datetime'],dbKey[key]['add'][0],putKey,'',url)
                    insert(conn2,'webdoc','daum',item['title'],'',item['datetime'],dbKey[key]['add'][0],putKey,'',url)

                    if dbResult:
                        data["meta"]["is_end"] = True;break
                    else:
                        insertNum = insertNum+1
                finally:
                    conn.close()
                    conn2.close()
            if  data["meta"]["is_end"] == False:
                apiStartNum = apiStartNum + 1
            else:
                break
    except:
        pass

    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    print("다음 web 크롤링 시작")
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '닥터프리즈너' or dbKey[k]['add'][0] == '국민여러분':
            startCrawling(k)
    print("다음 web 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
