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

cnt_osp = 'filecity'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                cnt_num = url.split('idx=')[1]
                idx = {
                    'idx': cnt_num,
                    'link': 'list',
                    'type': 'layer'
                }
                url2 = "https://filecity.kr/html/view2.html"
                post_two  = s.post(url2, data=idx)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                if soup.find('ul', 'clearfix icon_alliance') or soup.find('ul', 'clearfix icon_alliance '):
                    cnt_chk = 1
                if soup.find('ul', 'clearfix icon_sale'):
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filecity check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filecity check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
