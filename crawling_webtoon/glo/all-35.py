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
    link = 'https://all-35.net/bbs/group.php?gr_id=web_ing'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', id=re.compile("tab-+"))

        try:
            for item in div:
                div = item.find_all('div', 'post-row')
                for item in div:
                    url =  item.find('div', 'post-subject').find('a')['href']
                    title = item.find('div', 'post-subject').find('a', 'title').text.strip()
                    title_check = titleNull(title)

                    a = 0;pageCheck = True
                    page_url = url+'&spage='
                    while pageCheck:
                        a = a+1
                        if a == 50:
                            break
                        r = requests.get(page_url+str(a))
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        li = soup.find('ul', 'episode-list').find_all('li')
                        if len(li) < 2:
                            pageCheck=False;break

                        for item in li:
                            craw_url = item.find('a')['href'].split("&spage=")[0].strip()
                            title_numCh = titleNull(item.find('div', 'episode-title').text.strip())
                            title_num = title_numCh.replace(title_check, '').split("화")[0].strip()

                            data = {
                                'craw_osp_id': 'all-35',
                                'craw_domain': 'net',
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

    print("all-35 크롤링 시작")
    startCrawling()
    print("all-35 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
