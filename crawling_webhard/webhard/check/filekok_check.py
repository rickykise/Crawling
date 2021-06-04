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
from bs4 import BeautifulSoup as bs

cnt_osp = 'filekok'
checkNum = '2'

Page = {
    'act': 'get_token'
}

def main(url):
    token = ''
    token = ''
    with requests.Session() as s:
        login_req = s.post('http://www.filekok.com/ajax_controller.php', data=Page)
        soup = bs(login_req.text, 'html.parser')
        text = str(soup)
        token = text.split('{"result":"')[1].split('","')[0]

    LOGIN_INFO = {
        'browser': 'pc',
        'isSSL': 'Y',
        'mb_id': 'up0001',
        'mb_pw': 'up0001',
        'repage': 'reload',
        'token': token,
        'url': '/main/module/loginClass.php',
        'url_ssl': 'https://ssl.filekok.com/loginClass.php'
    }
    with requests.Session() as s:
        login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')

        try:
            post_one  = s.get(url)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0

            if soup.find_all('td', 'txt')[4].find('img'):
                jehu = soup.find_all('td', 'txt')[4].find('img')['alt']
                if jehu == '제휴컨텐츠':
                    cnt_chk= 1
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
