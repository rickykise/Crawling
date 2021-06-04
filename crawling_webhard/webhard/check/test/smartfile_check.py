import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from checkFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

cnt_osp = 'smartfile'
checkNum = '2'

LOGIN_INFO = {
    'Frame_login': 'Ok',
    'keep': 'Y',
    'm_id': 'unionct@naver.com',
    'm_pwd': 'up0001'
}

def main(url):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')

    try:
        with requests.Session() as s:
            headers = {'Cookie': '_ga=GA1.3.1872265032.1545795773; PHPSESSID=8ufueasbsb9evacap4qh0tsnb7; _gid=GA1.3.1221747159.1545888942; 046dd99d5c62a46485c88ba0022a8fa7=aWlzNDBAb3JnaW8ubmV0; 6c34d27f7f10a8246fb9b8bc6169dc1c=MTU0NTk3NTM2Mg%3D%3D; mecross_box_3333=5015711; storm_sale=F; Nnum=3; _gat=1; wcs_bt=79d0ffc89b3d5:1545894152'}
            login_req = s.post('http://smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO, headers=headers)

            r = s.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            print(soup)
            table = soup.find('table', summary='컨텐츠정보표').find('tbody')
            cnt_chk = 0

            if table.find_all('td')[2].find('img'):
                jehu = table.find_all('td')[2].find('img')['title']
                if jehu == '제휴':
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

    print("smartfile 체크2 크롤링 시작")
    for u in getUrl:
        main(u)
    print("smartfile 체크2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
