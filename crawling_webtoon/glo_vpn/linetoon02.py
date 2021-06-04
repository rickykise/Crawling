import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = 'http://linetoon02.com/?week='+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', id='container').find_all('li')

        try:
            for item in li:
                url = 'http://linetoon02.com'+item.find('a')['href']
                title = item.find('img')['alt']
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'tbl_wrap').find_all('li')

                for item in li:
                    craw_url = 'http://linetoon02.com'+item.find('a')['href']
                    craw_url = urllib.parse.unquote(craw_url)
                    title_numCh = titleNull(item.find('h3').text.strip())
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()
                    if title_num.find("(완전판)") != -1:
                        title_num = title_num.split('(완전판)')[1].strip()

                    data = {
                        'craw_osp_id': 'linetoon02',
                        'craw_domain': 'com',
                        'craw_title': title,
                        'craw_site_url' : url,
                        'craw_url': craw_url,
                        'craw_title_num': title_num
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("linetoon02 크롤링 시작")
    site = ['월','화','수','목','금','토','일','열흘']
    for s in site:
        startCrawling(s)
    print("linetoon02 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
