#네이버 영화 예고편 저장소
import datetime,pymysql,time
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
        tableName = 'naver_videos_all'
        data = {
            'portal_title' : args[0],
            'url' : args[1],
            'writeDate' : args[2],
            'createDate' : now,
            'updateDate' : now
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
    div = soup.find('div', 'end_container')

    dateCheck = div.find('div', 'video_watch open').find('div', 'title_info').find('span','date').text.strip().split("등록")[1]
    date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d.").strftime('%Y-%m-%d %H:%M:%S')

    data = {
        'writeDate' : date
    }
    # print(data)
    return data

def startCrawling():
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        link = 'http://tv.naver.com/navermovie/clips'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        for i in range(0, 3) :
            try:
                driver.find_element_by_xpath('//*[@id="cds_flick"]/div/div[3]/div/div/div/div[2]/div[3]/a').click()
                time.sleep(3)
                i +=1
            except:
                break
        html = driver.find_element_by_class_name("cds_flick").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        div = soup.find_all('div',  class_='_MM_CARD')

        for items in div:
            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            title = items.find('dt', 'title').find('a').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace("\u200b", "")
            href = 'http://tv.naver.com' + items.find('dt', 'title').find('a')['href']
            timech = items.find('dd', 'meta').find('span', 'time').text
            if timech == '1주 전':
                break
            resultData = getContents(href)

            data = {
                'portal_title' : title,
                'url' : href,
                'writeDate' : resultData['writeDate'],
                'createDate' : now,
                'updateDate' : now
            }
            print(data)

            # conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            # try:
            #     curs = conn.cursor(pymysql.cursors.DictCursor)
            #     dbResult = insert(conn,data['portal_title'],data['url'],data['writeDate'],data['createDate'],data['updateDate'])
            #     if dbResult:
            #         return False
            # finally :
            #     conn.close()
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("네이버영화 동영상 URL 크롤링 시작")
    startCrawling()
    print("네이버영화 동영상 URL 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
