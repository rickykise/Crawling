# 네이버 검색 Open API - 뉴스 검색
import datetime,time,pymysql
from bs4 import BeautifulSoup
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *

def startCrawling(mitem):
    apiStartNum = 1;insertNum = 0;check = False;key = mitem[0]+" "+mitem[1];paramKey = None
    print("키워드 : "+key)
    try:
        while apiStartNum < 1000:
            data = searchNAPI('news',key,'100',str(apiStartNum),'date')
            if len(data['items']) == 0: break
            for item in data['items']:
                conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                try:
                    # item['title'] = setText(item['title'],0) # 제목
                    # item['title'] = (len(item['title']) > 100) and item['title'][:96]+"…" or item['title']
                    item['title'] = item['title'].replace("&quot;","").replace("<b>;","").replace("<b>","").replace("</b>","").replace("amp;","")
                    item['description'] = setText(item['description'],1) # 내용
                    item['pubDate'] = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
                    dbKey = getSearchKey(conn,curs)
                    putKey = getPutKeyword(item['title'],item['description'],addAll)
                    putKey = (putKey == '') and 'press' or putKey
                    mainKey = (putKey != 'press') and getMainKey(conn,putKey) or ''
                    getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
                    getMainTileKeyworda = getMainTileKeyword(conn,curs)
                    MedianameUrl = getMedianameUrl(conn,curs)

                    newsTitle_keyword = checkMaintitle_key(mainKey, getMainTileKeyworda)
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

                    mediaUrl = checkMedianameUrl(mitem[0], item['link'], MedianameUrl)
                    media_name = mediaUrl['m']
                    url = mediaUrl['u']

                    if media_name != None and url != None: break

                    try:
                        if item['link'].find('/video/') != -1:
                            item['uid'] = item['link'].split('/video/')[-1]
                        elif item['link'].find('uid=') != -1:
                            item['uid'] = None
                        elif item['link'].find('aid=') != -1:
                            item['uid'] = None
                        elif item['link'].find('?') != -1:
                            num = None
                            print(item['link'])
                            if item['link'].find('id=') != -1:
                                numlst = [i for i in item['link'].split('?')[1].split('&') if i.find('id=') != -1]
                                num = (len(numlst) > 1) and [i for i in numlst if i.find('a') != -1][0] or numlst[0]
                            elif item['link'].find('volumeNo=') != -1:
                                numlst = [i for i in item['link'].split('?')[1].split('&') if i.find('volumeNo=') != -1]
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

                    media_subname = 'naver'
                    if item['link'].find('naver') == -1:
                        media_subname = 'out'

                    MediaMainname = getMediaMainname(conn,curs)
                    media_main = 0
                    medianameMainname = checkMediaKeyMedianame(mitem[0],MediaMainname)
                    if medianameMainname == True:
                        media_main = 1

                    if len(item['uid']) >= 15:
                        item['uid'] = None

                    for k in dbKey.keys():
                        result = checkKeyword(item['title'],item['description'],dbKey[k]['add'],dbKey[k]['del'],paramKey)
                        if result:
                            putKey = getPutKeyword(item['title'],item['description'],dbKey[k]['add'])
                            dbResult = insert(conn,'reporter',mitem[0],item['title'],item['description'],item['pubDate'],dbKey[k]['add'][0],putKey,k_type,item['link'],mitem[1],Mrank,item['uid'],media_subname,media_main)
                        else:
                            putKey = getPutKeyword(item['title'],item['description'],addAll)
                            putKey = (putKey == '') and 'press' or putKey
                            mainKey = (putKey != 'press') and getMainKey(conn,putKey) or ''
                            dbResult = insert(conn,'reporter',mitem[0],item['title'],item['description'],item['pubDate'],mainKey,putKey,k_type,item['link'],mitem[1],Mrank,item['uid'],media_subname,media_main)
                            insert(conn2,'reporter',mitem[0],item['title'],item['description'],item['pubDate'],mainKey,putKey,k_type,item['link'],mitem[1],Mrank,item['uid'],media_subname,media_main)
                        if dbResult:
                            check=True;break
                        else:
                            insertNum = insertNum+1
                finally:
                    conn.close()
                    conn2.close()
            if check: break
            apiStartNum = apiStartNum + 100
    except:
        pass

    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    reporter = getSearchReporter(conn,curs)
    addAll = getAddKeyword(conn,curs)
    conn.close()
    print("네이버 기자 뉴스 크롤링 시작")
    for m in reporter:
        startCrawling(m)
    print("네이버 기자 뉴스 크롤링 끝")
    print("==============================")
    print("--- %s seconds ---" %(time.time() - start_time))
