import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(url, chekc_item):
    i = 0;check = True;checkNum = 0;chUrl="";reUrl=""
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # checkDate = chekc_item[0]
    # limitDate = str(chekc_item[0]  + timedelta(30))
    # if now < limitDate:
    # try:
    if url.find('toutiao.com') != -1 or url.find('v.ifeng.com') != -1:
        if url.find('toutiao.com') != -1:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Host': 'www.toutiao.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            with requests.Session() as s:
                r = s.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                if text.find('404') != -1:
                    checkNum = 1
                    # dbUpdate(checkNum,now,url)
                else:
                    chUrl = r.url
                    if chUrl.find('http://') != -1:
                        chUrl = chUrl.split('http://')[1].strip()
                    elif chUrl.find('https://') != -1:
                        chUrl = chUrl.split('https://')[1].strip()
                    if url.find('http://') != -1:
                        reUrl = url.split('http://')[1].strip()
                    elif url.find('https://') != -1:
                        reUrl = url.split('https://')[1].strip()

                    if reUrl != chUrl:
                        print("원본 : ",reUrl)
                        print("변경 : ",chUrl)
                        print("=================================")
                        # checkNum = 1
                        # dbUpdate(checkNum,now,url)
                    else:
                        print("원본 : ",reUrl)
                        print("변경 : ",chUrl)
                        print("=================================")
                        # dbUpdate(checkNum,now,url)
        elif url.find('ifeng.com') != -1:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            with requests.Session() as s:
                r = s.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                reurl = soup.find_all('meta')[1]['content'].split('url=')[1]
                r = s.get(reurl, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                if text.find('404') != -1:
                    checkNum = 1
                    # dbUpdate(checkNum,now,url)
                else:
                    chUrl = r.url
                    if chUrl.find('http://') != -1:
                        chUrl = chUrl.split('http://')[1].strip()
                    elif chUrl.find('https://') != -1:
                        chUrl = chUrl.split('https://')[1].strip()
                    if url.find('http://') != -1:
                        reUrl = url.split('http://')[1].strip()
                    elif url.find('https://') != -1:
                        reUrl = url.split('https://')[1].strip()

                    if reUrl != chUrl:
                        checkNum = 1
                        print("원본 : ",reUrl)
                        print("변경 : ",chUrl)
                        print("=================================")
                    # else:
                        # print("원본 : ",reUrl)
                        # print("변경 : ",chUrl)
                        # print("=================================")
                        # dbUpdate(checkNum,now,url)
    else:

        r = requests.get(url)
        urlState = r.status_code
        if urlState == 200:
            chUrl = r.url
            if chUrl.find('http://') != -1:
                chUrl = chUrl.split('http://')[1].strip()
            elif chUrl.find('https://') != -1:
                chUrl = chUrl.split('https://')[1].strip()
            if url.find('http://') != -1:
                reUrl = url.split('http://')[1].strip()
            elif url.find('https://') != -1:
                reUrl = url.split('https://')[1].strip()

            if reUrl != chUrl:
                checkNum = 1
                print("원본 : ",reUrl)
                print("변경 : ",chUrl)
                print("=================================")
            # else:
            #     print("원본 : ",reUrl)
            #     print("변경 : ",chUrl)
            #     print("=================================")
            #     dbUpdate(checkNum,now,url)
            # dbUpdate(checkNum,now,url)
        else:
            checkNum = 1
                # dbUpdate(checkNum,now,url)
    # except:
    #     pass


if __name__=='__main__':
    start_time = time.time()
    getUrl = getHostUrl()

    print("f_list 재검수 시작")
    for u, c in getUrl.items():
        startCrawling(u, c)
    print("f_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
