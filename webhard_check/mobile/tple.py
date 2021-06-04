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

cnt_osp = 'tple'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                cnt_num = url.split('idx=')[1]
                url2 = 'http://www.tple.co.kr/storage/index.php?todo=view&source=W&idx='+cnt_num
                post_one  = s.get(url2)
                soup = bs(post_one.text, 'html.parser')
                cnt_chk = 0

                if soup.find('table', 'divNoticeTable'):
                    cnt_chk = 2
                else:
                    if soup.find('div', 'noticeArea'):
                        text = soup.find('div', 'noticeArea').text.strip()
                        if text.find('제휴업체') != -1:
                            cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_tple check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_tple check 크롤링 끝")
    print("m_--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
