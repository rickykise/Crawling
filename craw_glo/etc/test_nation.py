import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from similarwebFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from spyse import spyse

def startCrawling():
    osp_url = 'https://dongphim.net'
    url = osp_url.replace('https://', '').replace('http://', '')
    link = "https://www.alexa.com/siteinfo/" + url
    post_two  = requests.get(link)
    soup2 = bs(post_two.text, 'html.parser')
    osp_nat = soup2.find('section', 'country').find('li').find('div').text.encode('unicode-escape').decode('utf-8').split('\\xa0')[1].strip()
    osp_nat = change_Nat(osp_nat)
    print(osp_nat)

if __name__=='__main__':
    startCrawling()
