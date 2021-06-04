import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
import pymysql,time,datetime

def startCrawling():
    link = 'https://www.google.com/search?q=툰코&tbs=qdr&start=0'
    print(link)
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    if text.find('IP address: ') != -1:
        print('있다')
        time.sleep(50)
    div = soup.find_all('div', 'kCrYT')
    print(text)
    for item in div:
        # print(item)
        # print('========================')
        if item.find('a'):
            if item.find('span', 'FCUp0c') or item.find('span', 'r0bn4c'):
                continue
            title = item.find('div', 'BNeawe').text.strip()
            title_null = titleNull(title)

            # title 체크
            # googleCheck = googleCheckTitle(title_null, key, cnt_id)
            # if googleCheck == '' or googleCheck == None:
            #     continue

            url = item.find('a')['href'].split('url?q=')[1].split('&sa=')[0].replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
            url = urllib.parse.unquote(url)
            url = urllib.parse.unquote(url)

            # print(cnt_id)
            print(title)
            print(title_null)
            print(url)
            print("=================================")

            data = {
                'google_title': title,
                'google_url' : url,
                'osp_title': title
            }
            print(data)
            print("=================================")

                # dbResult = insertGoogle(data)
    # except:
    #     pass

if __name__=='__main__':
    start_time = time.time()

    print("google_webtoon 크롤링 시작")
    startCrawling()
    print("google_webtoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
