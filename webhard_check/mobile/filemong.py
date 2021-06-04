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

cnt_osp = 'filemong'

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'm.filemong.com',
    'Referer': 'https://m.filemong.com/contents/list.html?section=',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                post_one  = s.get(url, headers=headers, allow_redirects=False)
                soup = bs(post_one.text, 'html.parser')
                cnt_chk = 0

                cnt_price = soup.find('dl', 'dsc-view').find('dd').text.split("P")[0].replace(',', '').strip()
                title = soup.find('h1', 'hd-proftit').text.strip()
                title_null = titleNull(title)

                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                checkPrice = str(keyCheck['p'])
                if checkPrice == cnt_price:
                    cnt_chk = 1

                # print(title)
                # print('판매가 :', cnt_price)
                # print('정가 :', checkPrice)
                # print(cnt_chk)
                # print("=================================")
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filemong check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filemong check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
