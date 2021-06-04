import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from checkFun import *


cnt_osp = 'fileis'
checkNum = '3'

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://fileis.com/contents/index.htm',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '_ga=GA1.2.1547453409.1547110039; _gid=GA1.2.2142846955.1547110039; 1d67d4faecf228042770ca9c7c28f634=YTE3YWNkNTYzNmI4YjIyYjkwNGQyZWE1NmY0NmIzZTE%3D; 92b0eb816645a04605a0caee3c08e6f2=NjEuODIuMTEzLjE5Ng%3D%3D; openedIdx=a%3A4%3A%7Bi%3A13713476%3Bi%3A1547166743%3Bi%3A13700884%3Bi%3A1547166947%3Bi%3A12993257%3Bi%3A1547168937%3Bi%3A13050837%3Bi%3A1547168955%3B%7D'
}

def main(url):
    with requests.Session() as s:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        checkDate = getCntDate(url,checkNum,conn,curs).strftime('%Y-%m-%d %H:%M:%S')

        try:
            post_one  = s.get(url, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            cnt_chk = 0

            if soup.find('li', 'tit_le2'):
                cnt_chk = 1
        except:
            cnt_chk = 2

        if now >= checkDate:
            sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
            curs.execute(sql,(cnt_chk,url))
            conn.commit()

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(cnt_osp,checkNum,conn,curs)
    conn.close()

    print("fileis 체크3 크롤링 시작")
    for u in getUrl:
        main(u)
    print("fileis 체크3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
