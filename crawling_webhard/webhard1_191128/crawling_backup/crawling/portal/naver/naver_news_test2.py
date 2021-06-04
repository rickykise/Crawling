# 네이버 검색 Open API - 뉴스 검색
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from bs4 import BeautifulSoup
import datetime,time,pymysql

def startCrawling(key):
    apiStartNum = 1;paramKey = None;check=False;insertNum = 0
    if key == '공유' or key == '정유미': paramKey = key
    print("키워드 : "+key)
    while apiStartNum < 1000:
        data = searchNAPI('news',key,'100',str(apiStartNum),'date')
        if len(data['items']) == 0: break
        for item in data['items']:
            item['title'] = setText(item['title'],0) # 제목
            item['title'] = (len(item['title']) > 100) and item['title'][:96]+"…" or item['title']
            item['description'] = setText(item['description'],1) # 내용
            item['pubDate'] = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
            if item['pubDate'] < datetime.date.today().strftime('%Y-%m-%d'): continue

            result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
            if result:
                conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
                curs = conn.cursor(pymysql.cursors.DictCursor)
                getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
                getMainTileKeyworda = getMainTileKeyword(conn,curs)
                dbreporter = getReporter(conn,curs)
                MedianameUrl = getMedianameUrl(conn,curs)

                reporter = checkReporter(item['description'], dbreporter)
                # print(reporter)
                item['reporter_media_name'] = reporter['m']
                item['reporter_name'] = reporter['r']

                if item['reporter_media_name'] == None:
                    item['reporter_media_name'] = 'naver'

                mediaUrl = checkMedianameUrl(item['reporter_media_name'], item['link'], MedianameUrl)
                media_name = mediaUrl['m']
                url = mediaUrl['u']

                if media_name != None and url != None: break
                    # print('중복')

                # if item['reporter_media_name'].find(MedianameUrl.keys().values) != -1:
                #     print(item['reporter_media_name'])

                # for s in MedianameUrl.keys():
                #     if item['reporter_media_name'].find(s) != -1 :
                #         for m in MedianameUrl[s]:
                #             print(m)
                #             if item['link'].find(m) != -1 :



                newsTitle_keyword = checkMaintitle_key(dbKey[key]['add'][0], getMainTileKeyworda)
                if newsTitle_keyword['r'] != None:
                    k_type =getSearchTitleKeytpe(newsTitle_keyword['r'],conn,curs)
                    # print(k_type)
                else:
                    news_keyword = checkMainNewsKeyword(item['description'], getMainNewsKeyworda)
                    if news_keyword != None:
                        k_type = getSearchKeytpe(news_keyword['m'],news_keyword['r'],conn,curs)
                        # print(k_type)
                    else:
                        k_type = None
                try:
                    if item['link'].find('/video/') != -1:
                        item['uid'] = item['link'].split('/video/')[-1]
                    elif item['link'].find('?') != -1:
                        num = None
                        print(item['link'])
                        if item['link'].find('id=') != -1:
                            numlst = [i for i in item['link'].split('?')[1].split('&') if i.find('id=') != -1]
                            num = (len(numlst) > 1) and [i for i in numlst if i.find('a') != -1][0] or numlst[0]
                        elif item['link'].find('volumeNo=') != -1:
                            numlst = [i for i in item['link'].split('?')[1].split('&') if i.find('volumeNo=') != -1]
                            num = numlst[0]
                        elif item['link'].find('aid=') != -1:
                            numlst = [i for i in item['link'].split('?')[1].split('&') if i.find('aid=') != -1]
                            num = numlst[0]
                        elif item['link'].find('dummy=') != -1:
                            num = item['link'].split('?')[1].replace('dummy=','')

                        if num:
                            item['uid'] = re.sub('[^0-9]', '', num)
                        else:
                            item['uid'] = None
                    else:
                        item['uid'] = None
                except:
                    pass

                if item['uid'] != None:
                    Mrank = getSearchMrank(item['uid'],conn,curs)
                    # print(item['uid'])
                    # print(Mrank)
                else:
                    Mrank = None
                # try:
                #     putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
                #     dbResult = insert(conn,'media',item['reporter_media_name'],item['title'],item['description'],item['pubDate'],dbKey[key]['add'][0],putKey,k_type,item['link'],item['reporter_name'],Mrank,item['uid'])
                #     if dbResult:
                #         check=True;break
                #     else:
                #         insertNum = insertNum+1
                # finally:
                #     conn.close()
        if check: break
        apiStartNum = apiStartNum + 100

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 키워드 뉴스 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '경쟁영화':
        #     startCrawling(k)
        startCrawling(k)
    print("네이버 키워드 뉴스 크롤링 끝")
    print("==============================")
    print("--- %s seconds ---" %(time.time() - start_time))
