import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    cnt_writer = soup.find('title').text.split('- YouTube')[0].strip()
    dbYoutubeUpdate(cnt_writer,url)
    print(url)
    print(cnt_writer)
    print("=================================")


if __name__=='__main__':
    start_time = time.time()
    getKey = getyoutubetest()

    print("test 크롤링 시작")
    for u in getKey:
        startCrawling(u)
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
