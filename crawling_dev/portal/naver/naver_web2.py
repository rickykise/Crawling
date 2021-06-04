import datetime,pymysql,time
import sys,os
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    print("키워드 : "+key)
    insertNum = 0;start = 1;paramKey = None
    searchDay = datetime.datetime.now()
    searchDate1 = searchDay.strftime('%Y.%m.%d');searchDate2 = searchDay.strftime('%Y%m%d')
    encText = urllib.parse.quote(key)
    link = "https://search.naver.com/search.naver?where=webkr&query="+encText+"&opt_src=web&docid=0&lang=all&f=&srcharea=all&st=d&fd=2&display=10&domain=&filetype=none&sbni=&dtype=custom&dfrom="+searchDate1+"&dto="+searchDate1+"&sm=tab_pge&r=&research_url=&sbni_rootid=&nso=so%3Add%2Ca%3Aall%2Cp%3Afrom"+searchDate1+"to"+searchDate1+"&ie=utf8&start="
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        driver.get(link+str(start))
        time.sleep(3)
        while start < 600:
            html = driver.find_element_by_class_name('main_pack').get_attribute('innerHTML')
            soup = BeautifulSoup(html,"html.parser")
            ul = soup.find('ul', 'lst_total')
            findLI = ul.find_all("li")

            for item in findLI:
                try:
                    data = {
                        'title': item.find("a", 'link_tit').text.strip(),
                        'description': item.find('div', 'api_txt_lines').text.strip(),
                        'link': item.find("a", 'link_tit')['href'],
                        'date': searchDate1
                    }
                    data['description'] = setText(data['description'],1)
                    if data['link'].find('dcinside') != -1:
                        print(data)
                        print("=============================")

                except:
                    continue

                # if key == '공유' or key == '정유미': paramKey = key
                # result = checkKeyword(data['title'],data['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                # if not result: continue
                #
                # url = data['link']
                # if url is False: continue
                # elif url.find('joonggonara') != -1 and any(key == s for s in starKey): continue
                # elif url.find('linl.cf') != -1 and any(key == s for s in starKey): continue
                # elif url.find('modelvill.co.kr') != -1 and any(key == s for s in starKey): continue
                # elif url.find('8.uvhxnatmktj.cf') != -1 and any(key == s for s in starKey): continue
                # elif url.find('thamfarm.ga') != -1 and any(key == s for s in starKey): continue
                # elif url.find('g-enews') != -1: continue
                #
                # conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                # conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                # try:
                #     curs = conn.cursor(pymysql.cursors.DictCursor)
                #     curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                #     data['title'] = (len(data['title']) > 50) and data['title'][:47]+"…" or data['title']
                #     putKey = getPutKeyword(data['title'],data['description'],dbKey[key]['add'])
                #     putKeyType = getPutKeywordType(putKey,conn,curs)
                #     putKeyType = (putKeyType == None) and ' ' or putKeyType
                #
                #     if data['link'].find('dcinside') != -1:
                #         data['link'] = data['link'].replace('http://', 'https://')
                #         countNum = countNumget(data['link'])
                #         if countNum >= 1:
                #             continue
                #         board_number = data['link'].split('&no=')[1]
                #         dbResult = insertCommunity(conn,'dcinside',data['title'],data['description'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['link'],board_number)
                #         insertCommunity(conn2,'dcinside',data['title'],data['description'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['link'],board_number)
                #     else:
                #         dbResult = insert(conn,'webdoc','naver',data['title'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['link'])
                #         insert(conn2,'webdoc','naver',data['title'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['link'])
                #     if dbResult:
                #         break
                #     else:
                #         insertNum = insertNum+1
                # finally:
                #     conn.close()
                #     conn2.close()
            start = start+10
            driver.get(link+str(start))
            time.sleep(5)
    # except:
    #     pass
    finally:
        driver.close()
    # print("insert :",insertNum)
    # print("=============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbKey = getSearchKey(conn,curs)
    finally:
        conn.close()

    print("네이버 web 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("네이버 web 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
