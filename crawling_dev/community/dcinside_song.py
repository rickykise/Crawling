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
    'Cookie': 'PHPSESSID=77b945962e032dfb088b10a7b3b0072f; __utmc=118540316; __utmz=118540316.1578368789.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ck_lately_gall=8F%7C2JG%7Chj%7CJb%7CE9; __gads=ID=4fa7eaabd018c53b:T=1578368786:S=ALNI_Mb0RzPpVAxVALHSuFCCH5X7zskKvQ; last_alarm=1580714218; __utma=118540316.1484170209.1578368788.1578635810.1580714219.4; __utmb=118540316.2.10.1580714219; _ga=GA1.2.1484170209.1578368788; __utmt=1; ci_c=36a72830487d8cfc230bdbcb919b3f45; alarm_popup=1; p214Cap=1; wcs_bt=f92eaecbc22aac:1580714219; p214=1',
    'Host': 'gall.dcinside.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True;paramKey = None;insertNum = 0
    link = 'https://gall.dcinside.com/board/lists/?id=songhyekyo&page='
    while check:
        i = i+1
        if i == 100:
            break
        r = requests.get(link+str(i), headers=headers)
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

                try:
                    ip = item.find('td', 'gall_writer')['data-ip']
                except:
                    ip = ''

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                contents = soup.find('div', 'gallview_contents').find('div', style="overflow:hidden;").text.replace("\n","").replace("\t","").strip()
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

                dbKey = getSong()
                result = checkKeyword(data['title'],data['contents'],dbKey['송혜교']['add'],dbKey['송혜교']['del'],paramKey)
                if result:
                    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                        putKey = getPutKeyword(data['title'],data['contents'],dbKey['송혜교']['add'])
                        putKeyType = getPutKeywordType(putKey,conn,curs)
                        dbResult = insert(conn,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey['송혜교']['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        insert(conn2,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],dbKey['송혜교']['add'][0],putKey,putKeyType,data['url'],data['board_number'])
                        if dbResult:
                            check=True;break
                    finally:
                        conn.close()
                        conn2.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("디시인사이드 크롤링 시작")
    startCrawling()
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
