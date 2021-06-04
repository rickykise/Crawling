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

cnt_osp = 'dodofile'


headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://www.dodofile.com/board',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'opVal=1%7C1%7C0%7C1%7C0%7C0%7C0%7C0; PHPSESSID=49et3iqga9tssikfn4ggofme20; ACEFCID=UID-5C511801779491C04E7D2707; ACEUCI=1; _bbsInfoTab=Y; mi^c=2019-01-30%2012%3A20%3A37; mi^vi=JI0XN1IDQ1z7JKIQM2IEX125'
    }

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        # try:
        #     with requests.Session() as s:
        #         post_two  = s.get(url)
        #         c = post_two.content
        #         soup = bs(c.decode('euc-kr','replace'), 'html.parser')
        # except:
        #     cnt_chk = 2
        cnt_chk = 0
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("dodofile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("dodofile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
