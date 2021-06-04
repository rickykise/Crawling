import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {'vcID': 'undersd','vcPwd': 'undersd1234','x': '0','y': '0'}

def startCrawling():
    with requests.Session() as s:
        print(LOGIN_INFO)
        url = 'http://cp.fileis.com'
        s.get(url)
        cookie = str(s.cookies).split('Cookie ')[1].split(' ')[0]
        headers = {
            'Origin': 'http://cp.fileis.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': cookie
        }

        login_req = s.post(url, data=LOGIN_INFO, headers=headers)
        # login_req = s.post(url, params=LOGIN_INFO)
        post_one  = s.post('http://cp.fileis.com/list/list.php', headers=headers)
        soup = bs(post_one.text, 'html.parser')
        print(soup)

        # login_req = s.post('http://cp.fileis.com', data=LOGIN_INFO)
        # cookie = str(s.cookies).split('Cookie ')[1].split(' ')[0]
        # print(cookie)
        # cookies = {'Cookie': cookie}
        # login_req = s.post('http://cp.fileis.com', data=LOGIN_INFO, cookies=cookies)
        #
        # post_one  = s.get('http://cp.fileis.com/list/list.php')
        # soup = bs(post_one.text, 'html.parser')
        # print(soup)


if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
