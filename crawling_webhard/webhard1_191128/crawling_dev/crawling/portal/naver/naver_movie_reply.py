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
        sql = 'SELECT url FROM mobileent_data where ME_type="movie" and createDate >= curdate() order by createDate desc;'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def main(item):
    url = 'https://post.naver.com/viewer/postView.nhn?memberNo=31724756&volumeNo=9031364'
    print("url:", url)
    conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link= url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        if(link.find('m.post.naver') != -1):
            html = driver.find_element_by_class_name("sect_comment_wrap").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('span', 'u_cbox_count').text
            print('댓글:', reply)
            # elif driver.find_element_by_class_name("sect_post_detail_area").get_attribute('innerHTML'):
            #     html = driver.find_element_by_class_name("sect_post_detail_area").get_attribute('innerHTML')
            #     soup = BeautifulSoup(html, 'html.parser')
            #     reply = soup.find('em', 'cnt').text
            #     print('댓글:', reply)
        elif(link.find('post.naver') != -1):
            html = driver.find_element_by_class_name("sect_post_detail_area").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply_cnt = soup.find('button', '__comments_view').find('em').text
            reply = int(''.join(list(filter(str.isdigit,reply_cnt))))
            print('댓글:', reply)
        elif(link.find('m.blog') != -1):
            html = driver.find_element_by_class_name("section_w").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('a', 'btn_reply').find('em').text
            print('댓글:', reply)
        elif(link.find('m.entertain') != -1):
            html = driver.find_element_by_class_name("media_end_head_info_variety").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            span = soup.find('a', 'media_end_head_cmtcount_button').text
            reply = span.split("댓글")[1]
            print(reply)
        elif(link.find('entertain') != -1):
            html = driver.find_element_by_class_name("end_top_util").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply_cnt = soup.find('a', 'reply_count').text
            reply = reply_cnt.split("댓글")[1]
            print('댓글:', reply)
        elif(link.find('blog') != -1):
            link2 = link
            link3 = "http://m." + link2.split("https://")[1]
            driver.get(link3)
            html = driver.find_element_by_class_name("section_w").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('a', 'btn_reply').find('em').text
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
            print(data['url'])
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

    print("모바일영화 댓글 크롤링 시작")
    for u in getUrl:
        main(u)
    print("모바일영화 댓글 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
