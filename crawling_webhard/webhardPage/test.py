import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

# eyJub25jZSI6InByZWNlZGUiLCJpYXQiOjE1NDU4MTIyMjQsInR0bCI6MTQ0MCwiZXhwIjoxNTQ1ODEzNjY0fQ.KDhgHIx5fRFED_NJqWvbgBkrC2ZbcOcyRurubTFKpw2D8D52nF4gp5C8s4EHbL3aKkUmUTwcejJDj83XmMUd_Q
# eyJub25jZSI6InByZWNlZGUiLCJpYXQiOjE1NDU4NzQzNTIsInR0bCI6MTQ0MCwiZXhwIjoxNTQ1ODc1NzkyfQ.itikqbd9--3OMkfZThWKobNfpJhMaex-si3DHd2OYCoCUBhe9XhsCTmV0uKE1excqkGU1LI2ukgDbwaqGnH5ZA

LOGIN_INFO = {
    'browser': 'pc',
    'isSSL': 'Y',
    'mb_id': 'up0001',
    'mb_pw': 'up0001',
    'repage': 'reload',
    'token': 'eyJub25jZSI6InByZWNlZGUiLCJpYXQiOjE1NDU4NzQzNTIsInR0bCI6MTQ0MCwiZXhwIjoxNTQ1ODc1NzkyfQ.itikqbd9--3OMkfZThWKobNfpJhMaex-si3DHd2OYCoCUBhe9XhsCTmV0uKE1excqkGU1LI2ukgDbwaqGnH5ZA',
    'url': '/main/module/loginClass.php',
    'url_ssl': 'https://ssl.filekok.com/loginClass.php'
}
# http://www.filekok.com/ajax_controller.php
# act: get_token
#  no-cache
Page = {
    'act': 'get_token'
}

def startCrawling():
    with requests.Session() as s:
        login_req = s.post('http://www.filekok.com/ajax_controller.php', data=Page)
        soup = bs(login_req.text, 'html.parser')
        text = str(soup)
        token = text.split('{"result":"')[1].split('","')[0]
        print(token)


if __name__=='__main__':
    start_time = time.time()

    print("filekok 크롤링 시작")
    startCrawling()
    print("filekok 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
