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

cnt_osp = 'filehon'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                post_one  = s.get(url, headers=headers)
                soup = bs(post_one.text, 'html.parser')
                text = str(soup)
                cnt_chk = 0

                if soup.find('i', 'icon_alliance'):
                    jehu = soup.find('i', 'icon_alliance').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1
                if text.find('삭제된 자료') != -1:
                    cnt_chk = 2
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filehon check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filehon check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
