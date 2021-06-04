import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import random
from livvFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(idx, keyItem):
    print(idx)
    get_text = keyItem[0]
    get_text = get_text.split('<div class="content prdStat')[0].strip()
    Live_txt = get_text+'</div>'
    dbResult = dbTextUpdate(Live_txt, idx)

if __name__=='__main__':
    start_time = time.time()
    getT = getTextUrl()

    print("update 크롤링 시작")
    for u, i in getT.items():
        startCrawling(u, i)
    print("update 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
