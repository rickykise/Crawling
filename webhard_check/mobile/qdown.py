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

# 모바일url없음
cnt_osp = 'qdown'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                post_two  = s.get(url)
                c = post_two.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                text = str(soup)
                cnt_chk = 0

                if soup.find('td', 'infotable_td2').find('img'):
                    jehu = soup.find('td', 'infotable_td2').find('img')['title']
                    if jehu == '제휴':
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_qdown check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_qdown check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
