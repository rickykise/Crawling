import requests,re
import pymysql,time,datetime
import urllib.parse
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling():

if __name__=='__main__':
    start_time = time.time()

    print("m_applefile 크롤링 시작")
    site = ['DRA','MED','ANI','MVO']
    for s in site:
        startCrawling(s)
    print("m_applefile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
