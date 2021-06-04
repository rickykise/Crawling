import requests,re
import pymysql,time,datetime
import urllib.parse
from commonFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from datetime import date, timedelta

def startCrawling(key):
    i = 0;check = True
    key = key.replace(" ", "")
    print("키워드 : ",key)
    while check:
        try:
            i = i+1
            link = "http://www.syreop.com/b/star?page="+str(i)+"&string="+key
            r = requests.get(link)
            c = r.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            div = soup.find('div', 'postList postBlock postBoard')
            ul = soup.find_all("ul")[4]
            li = ul.find_all("li",class_=False)
            if len(li) == 0:print('게시물이 없습니다');check=False;break

            for item in li:
                timeCh = item.find('span', 'regdate').text.strip()
                if timeCh.find('2019-') != -1 or timeCh.find('2018-') != -1 or timeCh.find('2017-') != -1: check=False;break
                url = 'http://www.syreop.com' + item.find('a', 'listBlock')['href'].split("=")[0]+'='+key
                board_number = url.split("star/")[1].split("?string")[0]
                try:
                    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
                    driver.get(url)
                    time.sleep(2)
                    html = driver.find_element_by_class_name("postBlock").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')
                    title = soup.find('span', 'title').text.strip()
                    writer = soup.find('span', 'info_below').find('span').text.strip()
                    contents = soup.find('p').text.replace("\n","").replace("\t","").replace("\r","").replace("\xa0", "").strip()

                    date = soup.find('div', 'block-clearhead').find('span', 'info_top').text.strip()
                    if date.find('분')!= -1:
                        datech = date.split("분")[0]
                        datecheck = int(datech)
                        now = datetime.datetime.now()
                        date2 = now - datetime.timedelta(minutes=datecheck)
                        date = date2.strftime('%Y-%m-%d %H:%M:00')
                    elif date.find('시간')!= -1:
                        if date.find('한 시간 전')!= -1:
                            now = datetime.datetime.now()
                            datech = now - datetime.timedelta(hours=1)
                            date = datech.strftime('%Y-%m-%d %H:00:00')
                        else:
                            datech = date.split("시간")[0]
                            datecheck = int(datech)
                            now = datetime.datetime.now()
                            date2 = now - datetime.timedelta(hours=datecheck)
                            date = date2.strftime('%Y-%m-%d %H:00:00')
                    else:
                        pass

                    if date.find('에') != -1:
                        date = date.split("에")[0]
                except:
                    pass
                finally:
                    driver.close()

                data = {
                    'title' : title,
                    'url' : url,
                    'writer': writer,
                    'writerIp': '',
                    'board_number': board_number,
                    'contents' : contents,
                    'date': date
                }
                print(data)

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)

                if result is False: continue

                conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='union',port=3307,charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['title'],data['contents'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,'syreop',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    insert(conn2,'syreop',data['title'],data['contents'],data['writer'],data['writerIp'],data['date'],dbKey[mkey]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                    if dbResult:
                        check=False
                finally :
                    conn.close()
                    conn2.close()

        except:
            pass


if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("syreop 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("syreop 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
