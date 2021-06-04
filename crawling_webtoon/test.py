import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def startCrawling():
    # title = '대 :새dsfsd'
    # title2 = '대새'
    #
    # checkResult =  checkLen(title, title2)
    # print(checkResult)

    # url = 'http://www.5rs-wc16.com/'
    # r = requests.get(url)
    # urlState = r.status_code
    # c = r.content
    # soup = BeautifulSoup(c,"html.parser")
    #
    # if urlState == 200:
    #     if soup.find('title').text.find('유해정보사이트에 대한 차단') != -1:
    #         print('차단')
    #     else:
    #         print('정상')
    # print(soup)
    # print(urlState)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
