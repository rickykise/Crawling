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

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    # if now >= checkDate:
    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c.decode('euc-kr','replace'),"html.parser")
        cnt_chk = 0

        if soup.find('span', 'pl10').find('img'):
            jehu = soup.find('span', 'pl10').find('img')['src']
            if jehu.find('jehu.gif') != -1:
                cnt_chk = 1
    except:
        cnt_chk = 2
    print(url)
    print(checkNum,cnt_chk)
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
