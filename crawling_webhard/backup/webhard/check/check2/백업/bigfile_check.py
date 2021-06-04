import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from checkFun import *

cnt_osp = 'bigfile'
checkNum = '3'

def main(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")

    try:
        driver.get(url)
        time.sleep(2)
        htmll = driver.find_element_by_class_name('con_title').get_attribute('innerHTML')
        tags = BeautifulSoup(htmll,'html.parser')
        cnt_chk = 0

        if tags.find('span', 'con_ico').find('img'):
            img = tags.find('span', 'con_ico').find_all('img')
            if len(img) == 1:
                imgSrc = tags.find('span', 'con_ico').find('img')['src']
                if imgSrc.find('cooperation') != -1:
                    cnt_chk = 1
            elif len(img) == 2:
                imgSrc1 = tags.find('span', 'con_ico').find_all('img')[0]['src']
                imgSrc2 = tags.find('span', 'con_ico').find_all('img')[1]['src']
                if imgSrc1.find('cooperation') != -1 or imgSrc2.find('cooperation') != -1:
                    cnt_chk = 1
            elif len(img) == 3:
                imgSrc1 = tags.find('span', 'con_ico').find_all('img')[0]['src']
                imgSrc2 = tags.find('span', 'con_ico').find_all('img')[1]['src']
                imgSrc3 = tags.find('span', 'con_ico').find_all('img')[2]['src']
                if imgSrc1.find('cooperation') != -1 or imgSrc2.find('cooperation') != -1 or imgSrc3.find('cooperation') != -1:
                    cnt_chk = 1
    except:
        cnt_chk = 2

    if now >= checkDate:
        sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
        curs.execute(sql,(cnt_chk,url))
        conn.commit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl2(cnt_osp,checkNum,conn,curs)
    conn.close()

    print("bigfile 체크3 크롤링 시작")
    for u in getUrl:
        main(u)
    print("bigfile 체크3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
