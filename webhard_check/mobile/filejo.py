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

cnt_osp = 'filejo'

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
                post_two  = s.post(url, headers=headers)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                div = soup.find('div', 'datatext')
                cnt_chk = 0

                if div.find('ul').find_all('li')[2].find('img'):
                    img = div.find('ul').find_all('li')[2].find_all('img')
                    if len(img) == 1:
                        jehu = div.find('ul').find_all('li')[2].find('img')['src']
                        if jehu.find('icon_affily') != -1:
                            cnt_chk = 1
                    elif len(img) == 2:
                        jehu1 = div.find('ul').find_all('li')[2].find_all('img')[0]['src']
                        jehu2 = div.find('ul').find_all('li')[2].find_all('img')[1]['src']
                        if jehu1.find('icon_affily') != -1 or jehu2.find('icon_affily') != -1:
                            cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filejo check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filejo check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
