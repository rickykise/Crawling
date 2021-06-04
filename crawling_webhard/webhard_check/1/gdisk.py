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

cnt_osp = 'gdisk'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'idSave': '0',
                'm_id': 'up0001',
                'm_pwd': 'up0001',
                'm_pwd_load': '',
                'm_pwd_pass': '',
                'x': '27',
                'y': '29'
            }
            with requests.Session() as s:
                login_req = s.post('https://g-disk.co.kr/member/loginCheck2.php', data=LOGIN_INFO)
                cnt_num = url.split('idx=')[1]
                url2 = 'http://g-disk.co.kr/contents/view_top.html?idx='+cnt_num
                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                cnt_chk = 0

                if text.find('저작권자와의 제휴를') != -1:
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("gdisk check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("gdisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
