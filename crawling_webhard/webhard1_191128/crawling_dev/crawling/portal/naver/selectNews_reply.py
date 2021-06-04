import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

# url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT url FROM news_mail where (url like '%naver%' or url like '%daum%') and url not like '%stoo%' and replynum is null and createDate >= '2018-10-19 00:00:00' order by createDate desc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def main(item):
    url = item
    print("url:", url)
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link = url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        if(link.find('entertain') != -1 or link.find('news.naver.com/main') != -1):
            url2 = driver.current_url
            if(url2.find('entertain') != -1):
                html = driver.find_element_by_class_name("end_top_util").get_attribute('innerHTML')
                soup = BeautifulSoup(html, 'html.parser')
                reply_cnt = soup.find('a', 'reply_count').text
                reply = reply_cnt.split("댓글")[1]
                print('댓글:', reply)
            elif(url2.find('read') != -1):
                html = driver.find_element_by_class_name("u_cbox_head").get_attribute('innerHTML')
                soup = BeautifulSoup(html,'html.parser')
                reply = soup.find("span", "u_cbox_count").text.strip()
                print('댓글:', reply)
        elif(link.find('daum') != -1):
            html = driver.find_element_by_class_name("foot_view").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('em', 'num_count').text
            print('댓글:', reply)
        else:
            pass

        conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'reply': reply,
                'url' : link,
                'updateDate': now
            }
            print(data['url'])
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sql = "UPDATE news_mail SET replynum=%s, updateDate=%s WHERE url=%s;"
            curs.execute(sql,(data['reply'],data['updateDate'],data['url']))
            conn.commit()
        finally:
            conn.close()
    except:
        pass

    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("선택뉴스 댓글 크롤링 시작")
    for u in getUrl:
        main(u)
    print("선택뉴스 댓글 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
