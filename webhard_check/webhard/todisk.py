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

cnt_osp = 'todisk'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            headers = {
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie': 'appLogin=false; PHPSESSID=4513ea4563f87af45d1c741c755bb76a; log100=20190122; _ga=GA1.2.1070817977.1548124083; _gid=GA1.2.1882185260.1548124083; think_result=0; shacipher=Y; is_ctrl=Y; m_grade=1; mid=AvW14mtZM1qL1fJ2GITOhXQIdHDBrOCK2ZrmYSdgK2IKuZfVzCFenSbMnejn7xoCEB4DHWrPRmlFJLgNW1yQ1xMDSIffZSWpPXCkipajc3QUFkXX36T0TvaKcWc519lM; nick=up0001; Usr=up0001; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; LogChk=Y; _not100=Y; cidprt=Y; logtime=1548124086; logip=1028813252; vr=1'}
            with requests.Session() as s:
                post_two  = s.post(url, headers=headers)
                soup = bs(post_two.text, 'html.parser')
                table = soup.find('table', 'table2')
                cnt_chk = 0

                if table.find('td').find('img'):
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)
        
if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("todisk check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("todisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
