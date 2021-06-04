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

cnt_osp = 'pdpop'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Content-Length': '88',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'pdpopnet=0; connect_log=Y; _ga=GA1.2.1597594914.1553564520; _gid=GA1.2.1381734089.1553564520; _gat=1; cookie_id=up0001; age=45; auth=1; adult=1; uid=24412936; id=up0001%40pdpop.com; name=%EC%84%9C%EB%AF%BC%EC%8A%B9; clubsex=2; nickname=up0001; ero_birth=751031; ero_sex=2; domain=pdpop.com; PDPOP=LGbkAwc7pmb0BvWxLKEyVwgmBwL6VeaZipKQhlV7pmbmBvW1nJDvB3Z6BQbvZwD0ZGV5ZmLvB3Z6ZwbvnJDvB3Z6ZGL6VaIjZQNjZHOjMUOipP5wo20vB3Z6AwbvpTSmp3qxVwgmBwL0BvWyLmpmZQLkLwywZwt1ZQR1ZGZ5MzL3AQDmZGV0A2L4BTD1ZTSvZTEuAQyvZQp4AmDlZGHjBGZkBJR5AwIxAmuwVwgmBwD6Vz5uoJHvB3Z6BGbv7VFp66%2B87Vd5VwgmBwt6Vz5cL2ghLJ1yVwgmBwL6VaIjZQNjZFV7pmb1BvWfMKMyoPV7pmbkBvV5VwgmBwL6VzufMKMyoPV7pmblBvVjZFV7pmb1BvWvnKW0nPV7pmbkZQbvZGx3AF0kZP0mZFV7pmbmBvWuM2HvB2x6AQH7pmb1BvWuMUIfqPV7nGbkB3Z6AQbvLKI0nPV7nGbkB3Z6Zmbvp2I4VwgcBwV7pmb1BvWyoJScoPV7pmblZGbvpKqypwRlZmENpKqypwRlZmDhL29gVwgmBwL6VzEioJScovV7pmb5BvWjMUOipP5wo20vB3Z6ZGZ6VaOlo2McoTIsnJ1uM2HvB047sD%3D%3D; PHPSESSID=auuho4fi50um40trrf8h7equ60; changepay_notice=Y',
    'Host': 'm.pdpop.com',
    'Referer': 'http://m.pdpop.com',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        if url.find('m.pdpop') != -1:
            try:
                with requests.Session() as s:
                    cnt_num = url.split('idx=')[1].split('&')[0]
                    Data = {
                        'doc': 'board_view',
                        'idx': cnt_num,
                        'mPage': '1'
                    }
                    post_two  = s.get(url, headers=headers, data=Data)
                    soup = bs(post_two.text, 'html.parser')
                    text = str(soup)
                    cnt_chk = 0

                    if text.find('본 자료에는 제휴 컨텐츠') != -1:
                        cnt_chk = 1
            except:
                cnt_chk = 2
            dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_pdpop check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_pdpop check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
