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

def startCrawling(key, keyItem):
    searchKey = getGoogleSearch()
    for k in searchKey:
        keyword = key;cnt_id = keyItem[0];cnt_keyword='2';
        i = 0;check = True;googleKey = keyword+' '+k
        link = 'https://www.google.com/search?q='+googleKey+'&tbs=qdr&start='

        try:
            while check:
                r = requests.get(link+str(i))
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup)
                if text.find('IP address: ') != -1:
                    time.sleep(50)
                div = soup.find_all('div', 'kCrYT')

                for item in div:
                    if item.find('a'):
                        if item.find('span', 'FCUp0c') or item.find('span', 'r0bn4c'):
                            continue
                        title = item.find('div', 'BNeawe').text.strip()
                        title_null = titleNull(title)

                        # title 체크
                        googleCheck = googleCheckTitle(title_null, key, cnt_id)
                        if googleCheck == '' or googleCheck == None:
                            continue

                        url = item.find('a')['href'].split('url?q=')[1].split('&sa=')[0].replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
                        url = urllib.parse.unquote(url)
                        url = urllib.parse.unquote(url)

                        # url 체크
                        urlGet = getGoogleUrl()
                        urlCheck = checkGoogleUrl(url, urlGet)
                        if urlCheck['m'] == None:
                            continue

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'google',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'unitedstates',
                            'cnt_writer': '',
                            'origin_url': '',
                            'origin_osp': '',
                            'cnt_keyword_nat': None
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALLKey(data)

                i = i+10
                if i == 30:
                    check=False;break
        except:
            pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getGoogleNewKeyword()

    print("google 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("google 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
