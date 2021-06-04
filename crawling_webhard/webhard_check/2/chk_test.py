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
    # try:
    with requests.Session() as s:
        url = 'https://m.filecity.kr/contents/#tab=BD_MV&view=list&idx=23534735'
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

        print(soup)

        div = soup.find('div', 'cont_info clearfix')
        if div.find('ul', 'clearfix icon_alliance'):
            cnt_chk =1
    # except:
    #     cnt_chk = 2
    # dbUpdate(checkNum,cnt_chk,url)
    # print(url)
    # print(cnt_chk)

if __name__=='__main__':
    start_time = time.time()

    print("filecity check 크롤링 시작")
    main()
    print("filecity check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
