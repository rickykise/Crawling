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
        driver.get(link+str(start));time.sleep(3)
        try:
            total = int(driver.find_element_by_class_name('title_num').text.split(" / ")[1].replace(",","").replace("건",""))
        except:
            return
        if total > 600: total = 600
        while start < total:
            html = driver.find_element_by_class_name('sp_website').find_element_by_class_name("type01").get_attribute('innerHTML')
            soup = BeautifulSoup(html,"html.parser")
            findLI = soup.find_all("li")
            for item in findLI:
                info = item.find("dl")
                datech = ""
                if info.find('span', 'date'):
                    datech = info.find('span', 'date').text.strip()
                if datech.find('어제') != -1:
                    break
                try:
                    data = {
                        'title': info.find("dt").find("a").get_text(' ',strip=True).strip(),
                        'description': (info.find("dd","sh_web_passage") != None) and info.find("dd","sh_web_passage").get_text(' ',strip=True).strip() or '',
                        'link': info.find("dt").find("a")['href'],
                        'date': searchDate1
                    }
                except:
                    continue
                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['description'],dbKey[key]['add'],dbKey[key]['del'],paramKey)
                if not result: continue

                url = checkLink(data['link']);
                if url is False: continue
                elif url.find('joonggonara') != -1 and any(key == s for s in starKey): continue
                elif url.find('linl.cf') != -1 and any(key == s for s in starKey): continue
                elif url.find('modelvill.co.kr') != -1 and any(key == s for s in starKey): continue
                elif url.find('8.uvhxnatmktj.cf') != -1 and any(key == s for s in starKey): continue
                elif url.find('thamfarm.ga') != -1 and any(key == s for s in starKey): continue

                # conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                # try:
                #     curs = conn.cursor(pymysql.cursors.DictCursor)
                #     data['title'] = (len(data['title']) > 50) and data['title'][:47]+"…" or data['title']
                #     putKey = getPutKeyword(data['title'],data['description'],dbKey[key]['add'])
                #     putKeyType = getPutKeywordType(putKey,conn,curs)
                #     putKeyType = (putKeyType == None) and ' ' or putKeyType
                #     dbResult = insert(conn,'webdoc','naver',data['title'],'',data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['link'])
                #     if dbResult:
                #         break
                #     else:
                #         insertNum = insertNum+1
                # finally:
                #     conn.close()
            start = start+10
            driver.get(link+str(start));
            time.sleep(5)
    # except:
    #     pass
    finally:
        driver.close()
    print("insert :",insertNum)
    print("=============================")


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
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
