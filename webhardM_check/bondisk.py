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

cnt_osp = 'bondisk'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find('div', 'fileinfo_textarea')
            cnt_chk = 0

            price = div.find_all('li', 'info_a')[1].text.strip()
            if price.find('제휴') != -1:
                cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_bondisk check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_bondisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
