# 네이버 카페 벤츠 검색
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
        tableName = 'portal_data'
        data = {
            'portal_type': args[0],
            'portal_name': args[1],
            'portal_title': args[2],
            'deviceType': 1,
            'writer': args[3],
            'writeDate': args[4],
            'title_key': args[5],
            'keyword': args[6],
            'keyword_type': '',
            'url': args[7],
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

def main():
    print("키워드 : 벤츠")
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        link = 'http://cafe.naver.com/bmwdclub'
        #http://cafe.naver.com/bmwdclub?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=18624750%26search.media=0%26search.searchdate=all%26userDisplay=15%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.query=%BA%A5%C3%F7%26search.viewtype=title%26search.page=1
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        driver.find_element_by_name('query').send_keys('벤츠')
        driver.find_element_by_xpath('//*[@id="cafe-search"]/form/a').click()
        time.sleep(3)

        driver.switch_to_frame('cafe_main')
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        div = soup.find('div', 'article-board m-tcol-c')
        tr = div.find("table", "board-box").find("tbody").find_all("tr",align="center")

        for item in tr:
            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
            if item.find('td', 'board-line'):
                continue
            if item.find('td', 'board-list').find("span", "aaa").find('a', 'm-tcol-c') == None:
                continue
            title = item.find('td', 'board-list').find("span", "aaa").find('a', 'm-tcol-c').text
            board_number = item.find('td', 'board-list').find("span", "aaa").find('a', 'm-tcol-c')['href'].split("articleid=")[1].split("&")[0]
            href = 'http://cafe.naver.com/bmwdclub/' + board_number
            writerId =  item.find('span', 'wordbreak')['id'].split("article_")[1].split("_")[0]
            writer = item.find("span", "wordbreak").text + '(' +writerId + ')'
            # html = requests.get(href).text
            # driver.get(href)
            # driver.switch_to_frame('cafe_main')
            # page_main = driver.page_source
            # tags = BeautifulSoup(page_main,'html.parser')
            # dateCheck = tags.find('div', 'tit-box').find('div', 'fr').find('td', 'm-tcol-c date').text.strip()
            # datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')
            # date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')
            timech = item.find('td', 'view-count').text.strip()
            date = nowTime + ' ' +timech
            timecheck = timech.find(':')
            if timecheck == -1: check=False;break
            # print(date_test)

            data = {
                'portal_type': 'cafe',
                'portal_name': 'naver',
                'portal_title': title,
                'writer': writer,
                'writeDate': date,
                'title_key': '벤츠',
                'keyword': '벤츠',
                'url': href,
                'createDate': now,
                'updateDate':now
            }
            print(data)

            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                dbResult = insert(conn,data['portal_type'],data['portal_name'],data['portal_title'],data['writer'],data['writeDate'],data['title_key'],data['keyword'],data['url'],data['createDate'],data['updateDate'])
                if dbResult:
                    return False
            finally :
                conn.close()

    finally:
        driver.close()
    return True
    print("url:", url)

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("네이버 카페 벤츠 크롤링 시작")
    main()
    print("네이버 카페 벤츠 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
