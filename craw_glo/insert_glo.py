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

def startCrawling():
    idx = checkLink()
    for i in idx:
        # print(i)

        dbUpdate = dbUpdateIdx(i)

if __name__=='__main__':
    start_time = time.time()

    print("update 크롤링 시작")
    startCrawling()
    print("update 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
