import datetime,pymysql,time
import sys,os
import re
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link= 'https://movie.naver.com/movie/bi/mi/mediaView.nhn?code=157297&mid=40601#tab'
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        if(link.find('movie.naver.com/movie') != -1):
            html = driver.find_element_by_class_name("obj_section").get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            reply = soup.find('span', 'u_cbox_count').text.strip()
            print(reply)
    except Exception as e:
        print('에러:', e)  # wnat to know what error it is
        # conn = pymysql.connect(host='192.168.0.2',user='soas',password='qwer1234',db='union',charset='utf8')
        # try:
        #     curs = conn.cursor(pymysql.cursors.DictCursor)
        #     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     data = {
        #         'reply': reply,
        #         'url' : link,
        #         'updateDate': now
        #     }
        #     # print(data)
        #     placeholders = ', '.join(['%s'] * len(data))
        #     columns = ', '.join(data.keys())
        #     sql = "UPDATE mobileent_data SET reply_cnt=%s, updateDate=%s WHERE url=%s;"
        #     curs.execute(sql,(data['reply'],data['updateDate'],data['url']))
        #     conn.commit()
        # finally:
        #     conn.close()
    finally:
        driver.close()
    return True

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("모바일영화 댓글 크롤링 시작")
    # for u in getUrl:
    #     main(u)
    main()
    print("모바일영화 댓글 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
