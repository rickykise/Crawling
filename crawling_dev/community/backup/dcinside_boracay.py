# 디시인사이드 검색
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from commonFun import *
import time,pymysql,re,datetime
import requests

def startCrawling(key):
    print("키워드 : ",key)
    i=0;check = True;paramKey = None;insertNum = 0
    while check:
        try:
            i = i+1
            link = "http://gall.dcinside.com/mgallery/board/lists?id=boracay&s_type=search_all&s_keyword="+key+"&page="
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i))
            time.sleep(2)
            html = driver.find_element_by_id("kakao_search").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            tbody = soup.find('table', 'gall_list').find('tbody')
            tr = tbody.find_all('tr')

            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d')
                dateCh = item.find('td', 'gall_date').text.strip()
                dateCh = datetime.datetime.strptime(dateCh, "%y/%m/%d").strftime('%Y-%m-%d')
                if now > dateCh:
                    check=False;break
                board_number = item.find('a')['href'].split("&no=")[1]
                href = item.find('a')['href']

                r = requests.get(href)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', 'gallview_head clear ub-content')
                writerIp = ''

                title = soup.find('title').text.strip().split(" -")[0]
                writer = div.find('span', 'nickname')['title']
                if div.find('div', 'fl').find('span', 'ip'):
                    writerIp = div.find('div', 'fl').find('span', 'ip').text.strip().split("(")[1].split(")")[0]
                contents = soup.find('div', 'writing_view_box').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
                contents = setText(contents,0)
                date = soup.find('span', 'gall_date')['title']

                data = {
                    'title' : title,
                    'url' : href,
                    'writer': writer,
                    'writerIp': writerIp,
                    'board_number': board_number,
                    'contents' : contents,
                    'date': date
                }
                # print(data)

                if key == '공유' or key == '정유미': paramKey = key
                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

                if result:
                    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'dcinside',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
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

        print("insert :",insertNum)
        print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("디시인사이드 크롤링 시작")
    for k in dbKey.keys():
        if dbKey[k]['add'][0] == '더보이즈':
            startCrawling(k)
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
