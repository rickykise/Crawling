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

cnt_osp = 'fileguri'

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                result = getTitle(url)
                title = result[0][0]
                writer = result[0][1]
                url2 = 'http://m.fileguri.com/index.php?mode=content&cate=&search='+title
                post_two  = s.get(url2, headers=headers)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                div = soup.find('div', 'cont_txtlist')
                if div.find('li', 'nodata'):
                    cnt_chk = 2
                else:
                    li = div.find('ul').find_all('li')
                    for item in li:
                        cnt_writer = item.find_all('span', 'greyfont')[1].text.strip()
                        if cnt_writer == writer:
                            if item.find('span', 'bullet icon_img'):
                                cnt_chk = 1
                        else:
                            continue
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)
        # print(url)
        # print(cnt_chk)
        # print('==================================================')

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_fileguri check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_fileguri check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
