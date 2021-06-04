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

def startCrawling():
    i = 0;check = True
    link = 'https://mangafor.com/'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', id='categories-2').find('ul').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                title = item.find('a').text.strip()
                if title.find('–') != -1:
                    title = title.split('–')[1].strip()
                title_check = titleNull(title)

                a = 0;pageCheck = True
                page_url = url+'page/'
                while pageCheck:
                    a = a+1
                    if a == 10:
                        break
                    r = requests.get(page_url+str(a))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', id=re.compile("post-+"))
                    if len(div) < 1:
                        pageCheck=False;break

                    for item in div:
                        craw_url = item.find('a')['href']
                        craw_url = urllib.parse.unquote(craw_url)
                        title_numCh = titleNull(item.find('a')['title'])
                        title_num = title_numCh.split(title_check)[1].split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'mangafor',
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

    print("mangafor 크롤링 시작")
    startCrawling()
    print("mangafor 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
