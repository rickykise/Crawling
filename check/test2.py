import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import requests, json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from checkFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
    link = 'http://www.wedisk.co.kr/wediskNew/contentsView.do'

    data = {
        'contentsID': '21423243',
        'searchKey': '%7B%22searchType%22%3A%221%22%2C%22category%22%3A%2200%22%2C%22subCategory%22%3A%22%22%2C%22subKey%22%3A%22%22%2C%22keyword%22%3A%22%22%7D'
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'JSESSIONID=06B9462DBE3BDA7FF5DBE5411ABCDFEE; _ga=GA1.3.1997922284.1596689030; _gid=GA1.3.1000148076.1596689030; NSHcookie=200907221b0a72d26c6f0003; contentsListBar=true',
        'Host': 'www.wedisk.co.kr',
        'Referer': 'http://www.wedisk.co.kr/wediskNew/Home/main.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'X-Requested-With': 'XMLHttpRequest'
    }

    with requests.Session() as s:
        post_one  = s.post(link, headers=headers, data=data)
        c = post_one.content
        soup = BeautifulSoup(c,"html.parser")

        print(soup)
        time.sleep(2)

        url = 'http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=21423243'

        headers2 = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=06B9462DBE3BDA7FF5DBE5411ABCDFEE; _ga=GA1.3.1997922284.1596689030; _gid=GA1.3.1000148076.1596689030; NSHcookie=200907221b0a72d26c6f0003; contentsListBar=true',
            'Host': 'www.wedisk.co.kr',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        post_two  = s.get('http://www.wedisk.co.kr/wediskNew/contentsView.do?contentsID=21423243', headers=headers2, data=data)
        c = post_two.content
        print('실행')
        soup = BeautifulSoup(c,"html.parser")
        print(soup)

        # title = soup.find('div', 'register_title')['title']
        # table = soup.find('table').find('tbody')
        # td = table.find_all('tr')[1].find_all('div')[1]['class']
        # if len(td) == 1:
        #     cnt_chk = 1
        # else:
        #     cnt_chk = 0
        #
        # if td[0] != 'no_jw':
        #     td = table.find_all('tr')[1].find_all('div')[5]['class']
        #     if len(td) == 1:
        #         cnt_chk = 1
        #     else:
        #         cnt_chk = 0

        # print(title)
        # print("=================================")

if __name__=='__main__':
    start_time = time.time()

    print("wedisk check 크롤링 시작")
    main()
    print("wedisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
