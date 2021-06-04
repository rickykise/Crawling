import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from checkFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

cnt_osp = 'filekok'
checkNum = '2'

def main(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")

    try:
        driver.get(url)
        time.sleep(3)
        htmll = driver.find_element_by_id('wrap_pop').get_attribute('innerHTML')
        tags = BeautifulSoup(htmll,'html.parser')
        divtag = tags.find('div', id='left_contents')
        table = divtag.find('table', 'pop_base')
        cnt_chk = 0

        if table.find('tbody').find('td', 'txt').find('img'):
            img = table.find('tbody').find('td', 'txt').find('img')['alt']
            if img.find('제휴') != -1:
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
    getUrl = getSearchUrl(cnt_osp,checkNum,conn,curs)
    conn.close()

    print("filekok 체크2 크롤링 시작")
    for u in getUrl:
        main(u)
    print("filekok 체크2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
