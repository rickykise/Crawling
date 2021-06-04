#네이버 실시간 검색
import datetime,pymysql,time
from datetime import date, timedelta
import sys,os
import urllib.request
import requests,re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'search_data'
        data = {
            'portal_title': args[0],
            'portal_content': args[1],
            'portal_name': 'naver',
            'writer': args[2],
            'writeDate': args[3],
            'title_key': '더보이즈',
            'keyword': '더보이즈',
            'keyword_type': '',
            'url': args[4],
            'createDate': now,
            'updateDate':now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
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

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div', 'client-and-actions')

    date = div.find('span', 'metadata').text.strip()
    if date.find('오후') != -1:
        writeDatech = datetime.datetime.strptime(date, "오후 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
        clock = datetime.datetime.strptime(date, "오후 %H:%M - %Y년 %m월 %d일").strftime('%I')
        clock2 = int(clock)+12
        cl = str(clock2)
        writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
    else:
        writeDate = datetime.datetime.strptime(date, "오전 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'writeDate': writeDate
    }
    # print(data)
    return data

def getContents2(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    print(url)
    if url.find('news.naver') != -1:
        div = soup.find('div', 'end_ct').find('div', 'article_info')
        date = div.find('em').text.strip()

        if date.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(date, '%Y.%m.%d 오후 %I:%M').strftime('%Y-%m-%d %H:%M:%S')
            clock = datetime.datetime.strptime(date, "%Y.%m.%d 오후 %I:%M").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        else:
            writeDate = datetime.datetime.strptime(date, "%Y.%m.%d 오전 %I:%M").strftime('%Y-%m-%d %H:%M:%S')

    elif url.find('movie.naver') != -1:
        writeDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'writeDate': writeDate
    }
    # print(data)
    return data

def startCrawling():
    try:
        link = 'https://search.naver.com/search.naver?where=realtime&sm=tab_jum&query=정유미'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        # for i in range(0, 30) :
        #     try:
        #         driver.find_element_by_xpath('//*[@id="realTimeSearchBody"]/div[2]/div[2]/a').click()
        #         time.sleep(3)
        #         i +=1
        #     except:
        #         break
        html = driver.find_element_by_class_name("main_pack").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find("ul", 'type01')
        li = ul.find_all('li')

        for items in li:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if items.find('div', 'rt_btn_wrap') != None:
                content = items.find('span', 'cmmt _twitter').text.strip()
                writer = items.find('span', 'user_id').text.strip()
                url = items.find('span', 'cmmt _twitter')['data-src']
                resultData = getContents(url)

                data = {
                    'portal_title': '',
                    'portal_content': content,
                    'writer': writer,
                    'writeDate': resultData['writeDate'],
                    'url': url,
                    'createDate': now,
                    'updateDate':now
                }
                print(data)

            else:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # print(now)
                # title = items.find('dd', 'rt_org').find('a').find('img')['alt']
                title = items.find('div', 'org_info').find('a').text.strip()
                writer = items.find('dl').find('a').text.strip()
                content = items.find_all('dd')[1].find('a').text.strip()
                url = items.find('div', 'org_info').find('a')['href']
                resultData = getContents2(url)

                data = {
                    'portal_title': title,
                    'portal_content': content,
                    'writer': writer,
                    'writeDate': resultData['writeDate'],
                    'url': url,
                    'createDate': now,
                    'updateDate':now
                }
                print(data)

    # except:
    #     pass
    finally:
        driver.close()


if __name__=='__main__':
    start_time = time.time()

    print("네이버 실시간검색 크롤링 시작")
    startCrawling()
    print("네이버 실시간검색 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
