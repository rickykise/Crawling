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
    # url = http://phimb.net/phim/thien-than-noi-gian/
    title = 'Nhóm Nhảy Nhà Tù'
    title_check = titleNull(title)

    # 키워드 체크
    getKey = getKeyword()
    keyCheck = checkTitle(title_check, getKey)
    print('==================')
    print(keyCheck['m'])
    print('==================')
    # if keyCheck['m'] == None:
    #     continue


    # print(title)
    # print(title_check)

if __name__=='__main__':
    print('시작')
    startCrawling()
    print('끝')
