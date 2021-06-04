import datetime,pymysql,time
import urllib.request
import sys,os
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : "+key)
    insertNum = 0;start = 1;paramKey = None;check = True
    key = key.replace(' ', '')
    encText = urllib.parse.quote(key)
    link = "https://search.naver.com/search.naver?&where=news&query="+encText+"&sm=tab_pge&sort=2&photo=0&field=0&reporter_article=&pd=3&ds=2019.03.25&de=2019.04.22&docid=&nso=so:r,p:from20190325to20190422,a:all&mynews=0&cluster_rank=30&start="
    link2 = "&refresh_start=0"

    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link+str(start)+link2)
            start = start+10
            html = driver.find_element_by_class_name('_prs_nws').get_attribute('innerHTML')
            soup = BeautifulSoup(html,"html.parser")
            ul = soup.find('ul', 'type01')
            findLI = ul.find_all("li")
            for item in findLI:
                if item.find('a', '_sp_each_title'):
                    title = item.find('a', '_sp_each_title').text.replace("&quot;","").replace("<b>;","").replace("<b>","").replace("</b>","").replace("amp;","").strip()
                    contents = item.find('dd', class_=None).text.strip()
                    contents = setText(contents,1)
                    try:
                        writeDate = item.find('dd', 'txt_inline').text.split('  ')[1].split(' ')[0].strip()
                        writeDate = datetime.datetime.strptime(writeDate, '%Y.%m.%d.').strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        continue
                    url = item.find('a', '_sp_each_title')['href']
                    if url.find('g-enews') != -1 or url == None:
                        continue
                    media_name = item.find('dd', 'txt_inline').find('span', '_sp_each_source').text.strip()
                    # print(media_name)

                    result = checkKeyword(title,contents,dbKey[key]['add'],dbKey[key]['del'],paramKey)
                    if result:
                        conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
                        getMainTileKeyworda = getMainTileKeyword(conn,curs)
                        dbreporter = getReporter(conn,curs)
                        MedianameUrl = getMedianameUrl(conn,curs)
                        MediaKey = getMediaKey(conn,curs)
                        MediaKeySub = getMediaKeySub(conn,curs)

                        reporter = checkReporter(contents, dbreporter)
                        # print(reporter)
                        reporter_media_name = reporter['m']
                        reporter_name = reporter['r']

                        if reporter_media_name == None:
                            reporterSub = checkMedianame(contents, dbreporter)
                            reporter_media_name = reporterSub['m']
                            if reporter_media_name == None or reporter_media_name == "SBS" or reporter_media_name == "KBS" or reporter_media_name == "MBC" or reporter_media_name == "iMBC" or reporter_media_name == "JTBC":
                                medianameKey = checkMediaKeyUrl(url,MediaKey)
                                reporter_media_name = medianameKey['m']
                                if reporter_media_name == None:
                                    mediaKeywordName = checkMedianame(contents, MediaKeySub)
                                    reporter_media_name = mediaKeywordName['m']
                                    if reporter_media_name == None:
                                        reporter_media_name = 'naver'

                        newsTitle_keyword = checkMaintitle_key(dbKey[key]['add'][0], getMainTileKeyworda)
                        if newsTitle_keyword['r'] != None:
                            k_type =getSearchTitleKeytpe(newsTitle_keyword['r'],conn,curs)
                            # print(k_type)
                        else:
                            news_keyword = checkMainNewsKeyword(contents, getMainNewsKeyworda)
                            if news_keyword != None:
                                k_type = getSearchKeytpe(news_keyword['m'],news_keyword['r'],conn,curs)
                                # print(k_type)
                            else:
                                k_type = None

                        if url.find('naver') == -1:
                            media_subname = 'out'

                        MediaMainname = getMediaMainname(conn,curs)
                        media_main = 0
                        medianameMainname = checkMediaKeyMedianame(reporter_media_name,MediaMainname)
                        if medianameMainname == True:
                            media_main = 1

                        data = {
                            'media_name': media_name,
                            'title': title,
                            'contents': contents,
                            'writeDate': writeDate,
                            'url': url,
                            'media_subname': media_subname,
                            'media_main': media_main,
                            'title_key' : dbKey[key]['add'][0],
                            'k_type': k_type,
                            'uid': None
                        }
                        # print(data)
                        # print('===========================================')

                        try:
                            putKey = getPutKeyword(title,contents,dbKey[key]['add'])
                            dbResult = insert(conn,'media',data['media_name'],data['title'],data['contents'],data['writeDate'],dbKey[key]['add'][0],putKey,k_type,data['url'],None,None,data['uid'],data['media_subname'],data['media_main'])
                            if dbResult:
                                check=False;break
                            else:
                                insertNum = insertNum+1
                        finally:
                            conn.close()
    except:
        pass
    finally:
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("네이버 뉴스web 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '국민여러분':
            startCrawling(k)
    print("네이버 뉴스web 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
