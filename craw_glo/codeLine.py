import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter

def startCrawling():

    headers = {
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    data = {
        'color':'red',
        'delay':'5000',
        'h_percent':'0',
        'opacity':'1',
        'p_mode':'1',
        'size':'5',
        'w_percent':'0'
    }
    link = 'https://codeline.kr:58081/rest/start?key=union_test_key&api_key=d34cfe8ad3a949bf40e3fcebdf6250a6'
    r = requests.post(link, data=data, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")


if __name__=='__main__':
    startCrawling()
