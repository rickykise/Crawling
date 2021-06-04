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
                'Accept-Encoding' : 'gzip, deflate',
                'Accept-Language' : 'ko-KR',
                'Cache-Control' : 'no-cache',
                'Connection' : 'Keep-Alive',
                'Cookie': 'PHPSESSID=fjonm5nbraqmcblq7vaim43bp5; G_ENABLED_IDPS=google; viewContents=16582913',
                'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host' : 'www.filemaru.com',
                'Referer' : 'http://www.filemaru.com/',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest'
            }

            cnt_num = url.split('idx=')[1].strip()
            Page = {
                'ci': 'fjonm5nbraqmcblq7vaim43bp5',
                'idx': cnt_num
            }
            with requests.Session() as s:
                post_one  = s.post('https://www.filemaru.com/proInclude/ajax/view.php', data=Page, headers=headers)
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
    print("filemaru check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filemaru check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
