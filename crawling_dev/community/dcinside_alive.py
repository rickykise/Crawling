import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from commonFun import *
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insertAlive(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'community_dc'
        data = {
            'community_name': args[0],
            'community_title': args[1],
            'community_content': args[2],
            'community_writer': args[3],
            'community_writer_IP': args[4],
            'writeDate': args[5],
            'title_key': args[6],
            'keyword': args[7],
            'keyword_type': args[8],
            'url': args[9],
            'board_number': args[10],
            'createDate': now,
            'updateDate':now
        }

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
        else:
            result = True
            conn.rollback()
    finally:
        return result

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
    link = 'https://search.dcinside.com/post/p/'
    link2 = '/sort/latest/q/.EC.82.B4.EC.95.84.EC.9E.88.EB.8B.A4'
    while check:
        i = i+1
        if i == 100:
            break
        r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'sch_result_list').find_all('li')

        try:
            for item in li:
                title = item.find('a').text.strip()
                url = item.find('a')['href']
                board_number = url.split('no=')[1].strip()

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")

                contents = soup.find('div', 'gallview_contents').find('div', style="overflow:hidden;").text.replace("\n","").replace("\t","").replace('\xa0', '').strip()
                contents = setText(contents,0)
                writer = soup.find('span', 'nickname')['title']
                try:
                    ip = soup.find('div', 'gall_writer')['data-ip']
                except:
                    ip = ''
                date = soup.find('span', 'gall_date')['title']
                if date < '2020-06-23': check=False;break

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

                conn = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='horoscope',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    data['title'] = (len(data['title']) > 255) and data['title'][:240]+"…" or data['title']
                    dbResult = insertAlive(conn,'dcinside',data['title'],data['contents'],data['writer'],data['ip'],data['date'],'살아있다','살아있다','영화',data['url'],data['board_number'])
                    if dbResult:
                        check=True;break
                finally:
                    conn.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("디시인사이드 크롤링 시작")
    startCrawling()
    print("디시인사이드 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
