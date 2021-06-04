import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *

cnt_osp = 'smartfile'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'keep': 'Y',
                'm_id': 'Ie+av3IuqLcskZDGjP1JxM7FzabIbzDg2Ht2y/i/Kmo=||Il4lt5mbf9c6525b0e6a8000072887766021793',
                'm_pwd': '/ltwwmiPcL9NAET5eGSDvw==||VLzRtyG480d6bbce600c2ca0117e0b3e6fd84e0'
            }

            with requests.Session() as s:
                login_req = s.post('http://smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO)
                r = s.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find('table', summary='컨텐츠정보표').find('tbody')
                cnt_chk = 0

                if table.find_all('td')[2].find('img'):
                    jehu = table.find_all('td')[2].find('img')['title']
                    if jehu == '제휴':
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("smartfile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("smartfile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
