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

cnt_osp = 'filemaru'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            cnt_chk = 0
            # with requests.Session() as s:
            #     headers = {
            #         'Accept': 'application/json, text/javascript, */*; q=0.01',
            #         'Origin': 'http://www.filemaru.com',
            #         'X-Requested-With': 'XMLHttpRequest',
            #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            #     }
            #
            #     cnt_num = url.split('idx=')[1]
            #     url2 = 'http://www.filemaru.com/proInclude/ajax/view.php'
            #     Page = {
            #         'idx': cnt_num
            #     }
            #     post_one  = s.post(url2, data=Page, headers=headers)
            #     soup = bs(post_one.text, 'html.parser')
            #     text = str(soup)
            #     cnt_chk = 0

        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("filemaru check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filemaru check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
