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
    link = 'https://rktoon3.com/?view='+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        try:
            if site == "all":
                li = soup.find_all('li', 'comic_item')
                for item in li:
                    url = 'https://rktoon3.com'+item.find('a')['href']
                    title = item.find('p', 'tit_thumb_c').text.strip()
                    title_check = titleNull(title)

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    tr = soup.find('table', 'episode_list').find_all('tr', 'episode_tr')

                    for item in tr:
                        craw_url = 'https://rktoon3.com'+item.find('td', 'toon_title')['onclick'].split("href='")[1].split("'")[0]
                        title_num = item.find('td', 'toon_title').text.strip()

                        data = {
                            'craw_osp_id': 'rktoon3',
                            'craw_domain': 'com',
                            'craw_title': title,
                            'craw_site_url' : url,
                            'craw_url': craw_url,
                            'craw_title_num': title_num
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
            else:
                li = soup.find_all('li', 'li_comic_item')
                for item in li:
                    url = 'https://rktoon3.com'+item.find('a')['href']
                    title = item.find('span', 'title')['title']
                    title_check = titleNull(title)

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    tr = soup.find('table', 'episode_list').find_all('tr', 'episode_tr')

                    for item in tr:
                        craw_url = 'https://rktoon3.com'+item.find('td', 'toon_title')['onclick'].split("href='")[1].split("'")[0]
                        title_num = item.find('td', 'toon_title').text.strip()

                        data = {
                            'craw_osp_id': 'rktoon3',
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

    print("rktoon3 크롤링 시작")
    site = ['all','fin&k=all&sort=new']
    for s in site:
        startCrawling(s)
    print("rktoon3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
