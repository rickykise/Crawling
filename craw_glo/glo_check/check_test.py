import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(url):
    i = 0;check = True;checkNum = 0;
    print(url)
    # try:
    if url.find('toutiao.com') != -1 or url.find('v.ifeng.com') != -1:
        if url.find('toutiao.com') != -1:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Host': 'www.toutiao.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            with requests.Session() as s:
                r = s.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                if text.find('404') != -1:
                    print('404')
                else:
                    print('정상')
        elif url.find('ifeng.com') != -1:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            with requests.Session() as s:
                r = s.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                reurl = soup.find_all('meta')[1]['content'].split('url=')[1]
                r = s.get(reurl, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                if text.find('404') != -1:
                    print('404')
                else:
                    print('정상')
    else:
        r = requests.get(url)
        urlState = r.status_code
        if urlState == 200:
            print('정상')
        else:
            print('404')
    print('==========================================================')
    # except:
    #     pass


if __name__=='__main__':
    start_time = time.time()
    getUrl = getHostUrl()

    print("f_list 재검수 시작")
    for u in getUrl.items():
        startCrawling(u[0])
    print("f_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
