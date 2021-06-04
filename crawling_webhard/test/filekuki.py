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

LOGIN_INFO = {
    'passwd': 'up0001',
    'useridorig': 'up0001'
}

cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}

def main(url, cnt_price):
    try:
        with requests.Session() as s:
            getUrl = getSearchUrl(url,cnt_id)
            login_req = s.post('https://www.filekuki.com/db/db_login.jsp', data=LOGIN_INFO, cookies=cookies)
            post_one  = s.get(url, cookies=cookies)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            cnt_chk = 0
            table = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")

            title = soup.find('title').text.strip().split(" ◈")[0]
            cnt_price = table.split("쿠키")[0].replace(",","").strip()
            if soup.find('img', alt='특별할인'):
                priceCh = soup.find('strong').text.strip().replace("\n","").replace("\t","").replace("\xa0", "").replace(" ","").replace(",","")
                cnt_price = priceCh.split("→")[1].split("쿠키")[0].strip()

            if soup.find('img', alt='제휴'):
                cnt_chk = 1
            if text.find('filename') == -1:
                cnt_chk = 2
            print(title)
            print(url)
            print(cnt_chk)
            print(cnt_price)
            print('===============================')
    except:
        cnt_chk = 2
    # dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl()
    print("filekuki check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filekuki check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
