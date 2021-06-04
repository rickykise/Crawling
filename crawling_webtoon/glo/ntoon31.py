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
    link = 'https://www.ntoon31.com/'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        ul = soup.find_all('ul', 'homelist')

        try:
            for item in ul:
                li = item.find_all('li')
                for item in li:
                    if item.find('a'):
                        url = 'https://www.ntoon31.com'+item.find('div', 'section-item-title').find('a')['href']
                        title = item.find('div', 'section-item-title').find('a').text.strip()
                        title_check = titleNull(title)

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        tr = soup.find('table', 'episode_list').find('tbody').find_all('tr')

                        for item in tr:
                            craw_url = 'https://ntoon31.com'+item['onclick'].split("href='")[1].split("'")[0].strip()
                            span_text = item.find('div', 'div_epi_title').find('span').text.strip()
                            title_num = item.find('div', 'div_epi_title').text.replace(span_text, '').strip()

                            data = {
                                'craw_osp_id': 'ntoon31',
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

    print("ntoon31 크롤링 시작")
    startCrawling()
    print("ntoon31 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
