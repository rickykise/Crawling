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

def main():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    checkDate = '2020-09-03 02:52:52'
    url = 'https://filecity.kr/html/view2.html?idx=27632509'
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

                div = soup.find('div', 'cont_info clearfix')
                if div.find('ul', 'clearfix icon_alliance'):
                    cnt_chk = 1
                if div.find('ul', 'clearfix icon_sale'):
                    cnt_chk = 1
        except:
            cnt_chk = 2

        print(cnt_chk)
        # dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    # getUrl = getSearchUrl(cnt_osp)
    # print("filecity check 크롤링 시작")
    # for u, c in getUrl.items():
    #     c = '3' if c[0] == '0' else '2'
    #     main(u, c)
    main()
    print("filecity check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
