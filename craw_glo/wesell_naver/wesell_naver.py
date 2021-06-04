import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# db에 널을 text setting
def setText(s,t):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&apos;", "'")
    s = s.replace("&amp;", "&")
    s = s.replace("<b>","")
    s = s.replace("</b>","")
    s = s.replace("\r","")

    if t == 0:
        s = (len(s) > 49) and s[:47]+"…" or s
        s = remove_emoji(s)

    return s

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.0.132',user='wesellglobal',password='090612!23a',db='wesellglobal',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['portal_title'],data['portal_content'],data['url'],data['writer'],data['keyword'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_cafe'

        data = {
            'portal_title': args[0],
            'portal_content': args[1],
            'url': args[2],
            'writer': args[3],
            'keyword': args[4],
            'writeDate': now,
            'createDate': now
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

def startCrawling(key):
    i = 0;check = True;first_title = ''
    print("키워드 : "+key)
    link = 'https://cafe.naver.com/ca-fe/home/search/articles?q='+key+'&p='
    link2 = '&se=1&em=1&pr=1'
    try:
        while check:
            a = 0
            i = i+1
            driver = webdriver.Chrome("c:\python36\driver\chromedriver")
            driver.get(link+str(i)+link2)
            time.sleep(3)

            html = driver.find_element_by_class_name("SectionSearchArticles").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            li = soup.find('ul', 'ArticleList').find_all('li')

            for item in li:
                title = item.find('div', 'detail_area').find('a').text.strip()
                if title.find(key) == -1:
                    continue
                if title == first_title:
                    check=False;break
                if a == 0:
                    first_title = title
                    a = 1

                first_title = title
                url = item.find('div', 'detail_area').find('a')['href']
                cafe_name = url.split('.com/')[1].split('/')[0].strip()
                content = item.find('p', 'item_content').text.strip()
                content = setText(content,1)

                driver.get(url)
                time.sleep(5)

                html = driver.find_element_by_id('main-area').get_attribute('innerHTML')
                soup = BeautifulSoup(html,"html.parser")
                url_id = soup.find('iframe')['src'].split('clubid=')[1].strip()
                url_sub = url.split(cafe_name+'/')[1].split('?')[0].strip()
                cookie = url.split('art=')[1].strip()

                ajax_url = 'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/'+url_id+'/articles/'+url_sub+'?query=&art='+cookie

                r = requests.get(ajax_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                writer = text.split('nick":"')[1].split('"')[0].strip()

                data = {
                    'portal_title': title,
                    'portal_content' : content,
                    'url': url,
                    'writer': writer,
                    'keyword': key,
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("네이버 카페 크롤링 시작")
    key = ['위탁판매', '판매대행']
    for k in key:
        startCrawling(k)
    print("네이버 카페 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
