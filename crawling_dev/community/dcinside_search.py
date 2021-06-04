import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from commonFun import *
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Host': 'gall.dcinside.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key):
    print("키워드 : ",key)
    i = 0;check = True;paramKey = None;insertNum = 0
    link = "https://gall.dcinside.com/board/lists/?id=drama_new2&page="
    link2 = "&search_pos=&s_type=search_subject_memo&s_keyword="+key
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('tr', 'ub-content us-post')

        try:
            for item in div:
                notice = item['data-type']
                if notice == 'icon_notice':
                    continue
                title = item.find('td', 'gall_tit').find('a').text.strip()
                url = 'https://gall.dcinside.com'+item.find('td', 'gall_tit').find('a')['href']
                if url.find('&page=') != -1:
                    url = url.split('&page')[0]
                writer = item.find('span', 'nickname')['title']
                board_number = item.find('td', 'gall_num').text.strip()
                url = urllib.parse.unquote(url)

                try:
                    ip = item.find('td', 'gall_writer')['data-ip']
                except:
                    ip = ''

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                contents = soup.find('div', 'gallview_contents').find('div', 'write_div').text.replace("\n","").replace("\t","").strip()
                contents = setText(contents,0)
                date = soup.find('span', 'gall_date')['title']

                if date < datetime.datetime.now().strftime('%Y-%m-%d'): check=False;break

                data = {
                    'title' : title,
                    'url' : url,
                    'contents' : contents,
                    'date': date,
                    'writer': writer,
                    'ip': ip,
                    'board_number': board_number
                }
                # print(data)
                # print("=================================")

                result = checkKeyword(data['title'],data['contents'],dbKey[key]['add'],dbKey[key]['del'],paramKey)

                if result:
                    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey[key]['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        insert(conn2,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey[key]['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check=True;break
                    finally:
                        conn.close()
                        conn2.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("디시인사이드 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
