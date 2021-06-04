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
        sql = 'SELECT url FROM mobileent_data where ME_type="ent" and createDate >= curdate() order by createDate desc;'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def main(item):
    url = item
    print("url:", url)
    conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link= url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        if(link.find('listUrl=') != -1):
            html = driver.find_element_by_class_name("ui-overlay-a").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('span', 'u_re_cnt js-commentCount').text
            print('댓글:', reply)
        elif(link.find('m.entertain') != -1):
            html = driver.find_element_by_class_name("media_end_head_info_variety").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            span = soup.find('a', 'media_end_head_cmtcount_button').text
            reply = span.split("댓글")[1]
            print(reply)
        elif(link.find('read?') != -1):
            html = driver.find_element_by_class_name("end_ct").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.find('a', 'media_end_head_cmtcount_button').text
            reply_cnt = div.split("댓글")[1]
            reply = int(''.join(list(filter(str.isdigit,reply_cnt))))
            print('댓글:', reply)
        elif(link.find('tv.naver') != -1):
            html = driver.find_element_by_class_name("end_container").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('div', 'watch_btn').find('span','count _commentCount').text
            # reply = int(''.join(list(filter(str.isdigit,reply_cnt))))
            print('댓글:', reply)
        elif(link.find('tvcast') != -1):
            html = driver.find_element_by_class_name("end_container").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('div', 'watch_btn').find('span','count _commentCount').text
            # reply = int(''.join(list(filter(str.isdigit,reply_cnt))))
            print('댓글:', reply)
        elif(link.find('m.star') != -1):
            html = driver.find_element_by_class_name("subject_tm").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('a', 'cmt_upp').find('span').text
            print('댓글:', reply)
        elif(link.find('m.post') != -1):
            html = driver.find_element_by_class_name("sect_comment_wrap").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('span', 'u_cbox_count').text
            print('댓글:', reply)
        conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'reply': reply,
                'url' : link,
                'updateDate': now
            }
            # print(data)
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sql = "UPDATE mobileent_data SET reply_cnt=%s, updateDate=%s WHERE url=%s;"
            curs.execute(sql,(data['reply'],data['updateDate'],data['url']))
            conn.commit()
        finally:
            conn.close()
    except:
        pass

    finally:
        driver.close()
    return True

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("모바일연예 댓글 크롤링 시작")
    for u in getUrl:
        main(u)
    print("모바일연예 댓글 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
