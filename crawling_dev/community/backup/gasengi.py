import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div', id='view_conta')
    # print(div)

    dateCkeck = div.find_all('table')[0].find_all('span')[0].text.strip().split(": ")[1]
    datetime.datetime.strptime(dateCkeck, "%y-%m-%d %H:%M").strftime('%y-%m-%d %H:%M')
    date = datetime.datetime.strptime(dateCkeck, "%y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M:%S')

    contents = div.find('div', id='writeContents_sier').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
    # contents = div.find('div', id="writeContents").get_text(" ", strip=True).split("이미지 원본보기")[0].split("방송화면 캡처")[0].replace("\n","").replace("'","").replace("\t","").replace("\xa0", "").strip()

    data = {
        'contents': setText(contents,0),
        'date': date
    }
    # print(data)
    return data

def startCrawling(key):
    i = 0;check = True
    print("키워드 : ",key)
    while check:
        try:
            i = i+1
            link = "http://www.gasengi.com/main/board.php?bo_table=commu_etn&sca=&sfl=wr_subject&stx="+key+"&page="
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_class_name("board_list").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tr = soup.find("tbody").find_all("tr")

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if len(item) < 2:
                    check = False
                    print("게시물없음\n========================")
                    break
                if item.find('th') != None:
                    continue
                elif item.find('td', 'num').find('span'):
                    continue
                title = item.find('td', 'subject').find_all('a')[1].text.strip()
                hrefChek = item.find('td', 'subject').find_all('a')[1]['href'].split("..")[1]
                href = 'http://www.gasengi.com'+hrefChek
                board_number = href.split("&wr_id=")[1].split("&sca=")[0]
                writer = item.find('td', 'name').find('a').text.strip()
                timech = item.find('td', 'datetime').text.strip()
                timecheck = timech.find(':')
                if timecheck == -1: check=False;break
                print(timech)
                resultData = getContents(href)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: break

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': writer,
                    'writerIp': '',
                    'board_number': board_number,
                    'contents' : resultData['contents'],
                    'date': resultData['date'],
                }
                # print(data)

                conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'gasengi',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'gasengi',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False
                finally :
                    conn.close()
                    conn2.close()
        except:
            pass

        finally:
            driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("gasengi 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("gasengi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
