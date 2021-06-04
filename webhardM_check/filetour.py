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

cnt_osp = 'filetour'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            cnt_num = url.split('contents/')[1]
            url2 = 'http://www.filetour.com/front/contents/'+cnt_num
            r = requests.get(url2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            table = soup.find('table', 'show_table')
            cnt_chk = 0

            if table.find('span', 'b_blue_btn disp_ibl'):
                jehu = table.find('span', 'b_blue_btn disp_ibl').text.strip()
                if jehu == '제휴':
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filetour check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filetour check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
