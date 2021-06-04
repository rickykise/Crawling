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

LOGIN_INFO = {
    'email_tail': 'naver.com',
    'id': 'enjoy11@naver.com',
    'id_nm': 'enjoy11',
    'login_backurl': '',
    'mode': 'login_exec',
    'pw': 'enjoy11',
    'saved_pw': 'Y',
    'ssl_mobile_flg': '0',
    'wmode': 'noheader'
}

headers = {
    'Origin': 'http://m.smartfile.co.kr',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                login_req = s.post('http://m.smartfile.co.kr/member/login.html', data=LOGIN_INFO, headers=headers)
                cnt_num = url.split('idx=')[1]
                url2 = 'http://m.smartfile.co.kr/ajax/ajax.left.php'
                Page = {
                    'idx': cnt_num
                }
                post_two  = s.post(url2, headers=headers, data=Page)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                cnt_chk = 0

                if soup.find('div', 'info').find('p').find('font'):
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_smartfile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_smartfile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
