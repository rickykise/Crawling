#네이버 포스트
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

def startCrawling():
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    try:
        link = 'http://post.naver.com/search/post.nhn?keyword=%EB%B2%A4%EC%B8%A0&sortType=createDate.dsc&range=&term=d&navigationType=current'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(2)
        for i in range(0, 3) :
            try:
                driver.find_element_by_xpath('//*[@id="more_btn"]/button').click()
                time.sleep(3)
                i +=1
            except:
                break
        html = driver.find_element_by_class_name("lst_feed_wrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find_all("ul", class_='lst_feed')
        for items in ul:
            li = items.find_all("li", class_='_cds check_visible')
            for item in li:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item.find('strong', 'tit_feed ell').text.strip()
                writer = item.find('span', 'name').find('a').text.strip()
                href = 'http://post.naver.com' + item.find('div', 'image_area').find('a')['href']
                driver.get(href)
                time.sleep(2)
                page_main = driver.find_element_by_class_name("se_group").get_attribute('innerHTML')
                tags = BeautifulSoup(page_main,'html.parser')
                dateCheck = tags.find('p', 'se_detail').find('span', 'se_publishDate').text.strip()
                datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')
                date = datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M')

                data = {
                    'portal_type': 'post',
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
                # print(data)

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
    print("키워드 : 벤츠")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    conn.close()

    print("네이버 post 벤츠 크롤링 시작")
    startCrawling()
    print("네이버 post 벤츠 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")


# print(li)

# li = soup.find('ul', 'lst_feed').find_all('li')
# ul = soup.find_all("ul", class_='lst_feed')
# li = ul.find_all("li")


#     finally:
#             driver.close()
#
# if __name__=='__main__':
#     start_time = time.time()
#     startCrawling()
