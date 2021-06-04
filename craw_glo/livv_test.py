import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

# _csrf=_WSZbv3AmMGofeHSVR-M6CVQ; connect.sid=s%3AzTg5vrr8Xlcg78ZJkPbamgS581x4Baia.jqfT3c%2F4XlGbZLu7vfrUEB6S0WEOgzT%2F7U5sFAMAHW8; user=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6InJpY2t5a2lzZUBuYXZlci5jb20iLCJuYW1lIjoi7LWc7JiB7JqwIiwiaWF0IjoxNjEzNDUzOTY3LCJleHAiOjE2MTM0NTc1Njd9.3Shbvhi8VwdZc7LOuq4EeHYmFUXJr0JVMhEz1VKV7Qc
# _csrf=3xrs_W_JZDDnmC9eXd6s7iel; livv=s%3A2r57kn42vIjEBqfdRoIKTeJy77oo-CPh.qntUK%2Fnb5l%2FdeTW908dvBUTeEl%2BME%2BNb3vkNeR1cA74; user=
def startCrawling():
    headers = {
        'X-CSRF-Token': 'VT3ULBuw-UH7GSupy4oIpjAs5ZHvYvD-pdqU'
    }

    r = requests.post('http://www.livevery.co.kr/auth/info', headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    print(soup)


if __name__=='__main__':
    startCrawling()
