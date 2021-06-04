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

cnt_osp = 'sedisk'

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer': 'http://sedisk.com/storage.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'ACEFCID=UID-5C22F965D514161EE9381054; _ga=GA1.2.1287727625.1545974475; ptn=ksc0110; ACEUCI=1; _gid=GA1.2.1421021257.1547447786; evLayer=N; _gat=1'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                cnt_num = url.split('idx=')[1].split('&')[0]
                url2 = 'http://sedisk.com/storage.php?act=view&idx=' + cnt_num
                post_two  = s.post(url2, headers=headers)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                if soup.find_all('td', 'point_vol')[2].find('img'):
                    img = soup.find_all('td', 'point_vol')[2].find('img')['src']
                    if img.find('ico_jehu2') != -1:
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_sedisk check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_sedisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
