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
    try:
        while apiStartNum < 1000:
            data = searchNAPI('news',key,'100',str(apiStartNum),'date')
            if len(data['items']) == 0: break
            for item in data['items']:
                # item['title'] = setText(item['title'],0) # 제목
                # item['title'] = (len(item['title']) > 100) and item['title'][:96]+"…" or item['title']
                item['title'] = item['title'].replace("&quot;","").replace("<b>;","").replace("<b>","").replace("</b>","").replace("amp;","")
                # item['description'] = setText(item['description'],1) # 내용
                item['pubDate'] = datetime.datetime.strptime(item['pubDate'], '%a, %d %b %Y %H:%M:%S %z').strftime('%Y-%m-%d %H:%M:%S')
                if item['pubDate'] < datetime.date.today().strftime('%Y-%m-%d'): continue
                # if item['pubDate'] <'2018-09-18': continue

                result = checkKeyword(item['title'],item['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
                    getMainTileKeyworda = getMainTileKeyword(conn,curs)
                    dbreporter = getReporter(conn,curs)
                    MedianameUrl = getMedianameUrl(conn,curs)
                    MediaKey = getMediaKey(conn,curs)
                    MediaKeySub = getMediaKeySub(conn,curs)

                    reporter = checkReporter(item['description'], dbreporter)
                    # print(reporter)
                    item['reporter_media_name'] = reporter['m']
                    item['reporter_name'] = reporter['r']

                    if item['reporter_media_name'] == None:
                        reporterSub = checkMedianame(item['description'], dbreporter)
                        item['reporter_media_name'] = reporterSub['m']
                        if item['reporter_media_name'] == None or item['reporter_media_name'] == "SBS" or item['reporter_media_name'] == "KBS" or item['reporter_media_name'] == "MBC" or item['reporter_media_name'] == "iMBC" or item['reporter_media_name'] == "JTBC":
                            medianameKey = checkMediaKeyUrl(item['link'],MediaKey)
                            item['reporter_media_name'] = medianameKey['m']
                            if item['reporter_media_name'] == None:
                                mediaKeywordName = checkMedianame(item['description'], MediaKeySub)
                                item['reporter_media_name'] = mediaKeywordName['m']
                                if item['reporter_media_name'] == None:
                                    item['reporter_media_name'] = 'naver'

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

                    mediaUrl = checkMedianameUrl(item['reporter_media_name'], item['link'], MedianameUrl)
                    media_name = mediaUrl['m']
                    url = mediaUrl['u']
                    if media_name != None and url != None: break

                    try:
                        if item['link'].find('/video/') != -1:
                            item['uid'] = item['link'].split('/video/')[-1]
                        elif item['link'].find('uid=') != -1:
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

                    media_subname = 'naver'
                    if item['link'].find('naver') == -1:
                        media_subname = 'out'

                    MediaMainname = getMediaMainname(conn,curs)
                    media_main = 0
                    medianameMainname = checkMediaKeyMedianame(item['reporter_media_name'],MediaMainname)
                    if medianameMainname == True:
                        media_main = 1

                    if len(item['uid']) >= 15:
                        item['uid'] = None

                    item['description'] = setText(item['description'],1)

                    try:
                        # conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                        putKey = getPutKeyword(item['title'],item['description'],dbKey[key]['add'])
                        dbResult = insert(conn,'media',item['reporter_media_name'],item['title'],item['description'],item['pubDate'],dbKey[key]['add'][0],putKey,k_type,item['link'],item['reporter_name'],Mrank,item['uid'],media_subname,media_main)
                        # insert(conn2,'media',item['reporter_media_name'],item['title'],item['description'],item['pubDate'],dbKey[key]['add'][0],putKey,k_type,item['link'],item['reporter_name'],Mrank,item['uid'],media_subname,media_main)
                        if dbResult:
                            check=True;break
                        else:
                            insertNum = insertNum+1
                    finally:
                        conn.close()
                        # conn2.close()
            if check: break
            apiStartNum = apiStartNum + 100
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 키워드 뉴스 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '영화일반':
        #     startCrawling(k)
        startCrawling(k)
    print("네이버 키워드 뉴스 크롤링 끝")
    print("==============================")
    print("--- %s seconds ---" %(time.time() - start_time))
