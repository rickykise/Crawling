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

cnt_osp = 'filemaru'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Origin': 'http://m.filemaru.com',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
            cnt_num = url.split('.php')[1].strip()
            Page = {
                'idx': cnt_num
            }
            with requests.Session() as s:
                post_one  = s.post('https://m.filemaru.com/proInclude/ajax/view.php', headers=headers, data=Page)
                soup = bs(post_one.text, 'html.parser')
                text = str(soup)
                cnt_chk = 0

                jehu = text.split('fileAllianceChk" : "')[1].split('"')[0]
                if jehu == "Y":
                    cnt_chk = 1

        except:
            cnt_chk = 2

        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filemaru check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filemaru check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
