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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

cnt_osp = 'megafile'

LOGIN_INFO = {
    'login_backurl': '',
    'loginid': 'up0002',
    'passwd': 'up0002',
    'site': 'megafile.co.kr',
    'type': '',
    'url': 'http://m.megafile.co.kr/'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                login_req = s.post('http://m.megafile.co.kr/user/login_process.php', data=LOGIN_INFO)

                post_two = s.get(url, headers=headers)
                c = post_two.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                div = soup.find('div', id='fileinfo_text')
                cnt_chk = 0

                if soup.find('div', 'filetitle').find('img'):
                    jehu = soup.find('div', 'filetitle').find('img')['src']
                    if jehu.find('icon_copyright2') != -1:
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_megafile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_megafile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
