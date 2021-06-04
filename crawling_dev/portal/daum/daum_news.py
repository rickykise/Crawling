# 다음 뉴스 크롤링 - DB
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
import time,datetime,pymysql

def startCrawling(key):
    searchDate = datetime.datetime.now().strftime('%Y%m%d')
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    driver.get("https://search.daum.net/search?w=news&sort=recency&q="+key+"&cluster=n&DA=PGD&s=NS&a=STCF&dc=STC&pg=1&r=1&p=1&rc=1&at=more&sd="+searchDate+"000000&ed="+searchDate+"235959&period=u")
    try:
        print("키워드 :",key)
        check=False;paramKey = None;insertNum = 0
        if key == '공유' or key == '정유미':paramKey = key

        while True:
            html = driver.find_element_by_class_name('coll_cont').get_attribute("innerHTML")
            soup = BeautifulSoup(html,"html.parser")

            findLI = soup.find_all("li")
            for item in findLI:
                info = item.find("span",{"class":"date"})
                data = {
                    'title':item.find("a",{"class":"f_link_b"}).text,
                    'contents':item.find("p",{"class":"desc"}).text,
                    'url': info.find("a") and info.find("a")['href'] or item.find("a",{"class":"f_link_b"})['href'],
                    'pubDate':datetime.datetime.strptime(searchDate,'%Y%m%d'),
                    # 'media_name' : item.find('span', 'f_nb date').text.replace(" ","").split('|')[1].strip()
                    'media_name' : item.find('span', 'f_nb date').text.replace(" ","").replace("\n","").strip()
                }

                if data['media_name'].find('다음뉴스') != -1:
                    data['media_name'] = data['media_name'].split("|")[1].split("|")[0]
                else:
                    data['media_name'] = data['media_name'].split("|")[1]
                print(data['media_name'])
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    getMainNewsKeyworda = getMainNewsKeyword(conn,curs)
                    getMainTileKeyworda = getMainTileKeyword(conn,curs)
                    dbreporter = getReporter(conn,curs)
                    MedianameUrl = getMedianameUrl(conn,curs)
                    MediaKey = getMediaKey(conn,curs)
                    MediaKeySub = getMediaKeySub(conn,curs)

                    reporter = checkReporter(data['contents'], dbreporter)
                    # print(reporter)
                    reporter_media_name = reporter['m']
                    reporter_name = reporter['r']

                    if reporter_media_name == None:
                        reporterSub = checkMedianame(data['contents'], dbreporter)
                        reporter_media_name = reporterSub['m']
                        if reporter_media_name == None or reporter_media_name == "SBS" or reporter_media_name == "KBS" or reporter_media_name == "MBC" or reporter_media_name == "iMBC" or reporter_media_name == "JTBC":
                            medianameKey = checkMediaKeyUrl(data['url'],MediaKey)
                            reporter_media_name = medianameKey['m']
                            if reporter_media_name == None:
                                mediaKeywordName = checkMedianame(data['contents'], MediaKeySub)
                                reporter_media_name = mediaKeywordName['m']
                                if reporter_media_name == None:
                                    reporter_media_name = 'daum'

                    newsTitle_keyword = checkMaintitle_key(dbKey[key]['add'][0], getMainTileKeyworda)
                    if newsTitle_keyword['r'] != None:
                        k_type =getSearchTitleKeytpe(newsTitle_keyword['r'],conn,curs)
                        # print(k_type)
                    else:
                        news_keyword = checkMainNewsKeyword(data['contents'], getMainNewsKeyworda)
                        if news_keyword != None:
                            k_type = getSearchKeytpe(news_keyword['m'],news_keyword['r'],conn,curs)
                            # print(k_type)
                        else:
                            k_type = None

                    mediaUrl = checkMedianameUrl(reporter_media_name, data['url'], MedianameUrl)
                    media_name = mediaUrl['m']
                    url = mediaUrl['u']
                    if media_name != None and url != None: break

                    media_subname = 'daum'
                    if data['url'].find('daum') == -1:
                        media_subname = 'out'

                    MediaMainname = getMediaMainname(conn,curs)
                    media_main = 0
                    medianameMainname = checkMediaKeyMedianame(reporter_media_name,MediaMainname)
                    if medianameMainname == True:
                        media_main = 1

                    try:
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        dbResult = insert(conn,'media',data['media_name'],data['title'],data['contents'],data['pubDate'],dbKey[key]['add'][0],putKey,k_type,data['url'],reporter_name,None,None,media_subname,media_main)
                        insert(conn2,'media',data['media_name'],data['title'],data['contents'],data['pubDate'],dbKey[key]['add'][0],putKey,k_type,data['url'],reporter_name,None,None,media_subname,media_main)
                        if dbResult:
                            check=True;break
                        else:
                            insertNum = insertNum+1
                    finally:
                        conn.close()
                        conn2.close()
            if driver.find_element_by_class_name('result_message').get_attribute("class") == "result_message mg_cont hide":
                if driver.find_element_by_class_name('btn_next').get_attribute("class") != "ico_comm1 btn_page btn_next" or check:
                    break
                driver.find_element_by_class_name('btn_next').click();time.sleep(3)
            else:
                break
    except Exception as e:
        print("에러 : ",e)
    # except:
    #     pass
    finally:
        driver.close()

    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()
    print("다음 뉴스 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '경쟁영화':
        #     startCrawling(k)
        startCrawling(k)
    print("다음 뉴스 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
