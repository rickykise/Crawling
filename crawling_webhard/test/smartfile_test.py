import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import pyautogui
import pickle
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from webhardFun import *

def startCrawling(site):
    i = 0;a = 1;check = True
    url = 'http://smartfile.co.kr/index.php'
    try:
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(url)
        time.sleep(2)
        driver.find_element_by_id('login_m_id').send_keys('enjoy11@naver.com')
        driver.find_element_by_id('login_m_pw').send_keys('enjoy11')
        time.sleep(1)
        pyautogui.hotkey('enter')
        time.sleep(2)
        pyautogui.hotkey('enter')
        time.sleep(2)

        cookies = driver.get_cookies()
        print(cookies)

        cookName = str(cookies).split("'name': '")[3].split("', '")[0]
        cookValue = str(cookies).split("'value': '")[3].split("'")[0]
        getCookiescheck = cookName+'='+cookValue
        print(getCookiescheck)
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
    # except:
    #     pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("smartfile 크롤링 시작")
    # site = ['MVO','DRA','MED','ANI']
    site = ['MVO']
    for s in site:
        startCrawling(s)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
