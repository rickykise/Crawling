import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    link = 'https://www.myktoon.com/web/webtoon/works_list.kt'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    article = soup.find('div', 'week_all').find_all('article')

    for item in article:
        li = item.find('ul').find_all('li')
        for item in li:
            url = item.find('a')['href']
            title = item.find('div', 'info').find('strong').text.strip()
            title_check = titleNull(title)
            conNum = url.split('worksseq=')[1].strip()

            i = 0;check = True
            host_url = 'https://v2.myktoon.com/web/works/times_list_ajax.kt'
            while check:
                try:
                    if i == 550:
                        break
                    Data = {
                        'sorting': 'up',
                        'startCnt': i,
                        'turmCnt': '50',
                        'worksseq': conNum
                    }
                    r = requests.post(host_url, data=Data)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)
                    json_obj = json.loads(text)
                    i = i+50
                    if json_obj['response'] == []:
                        i = 0
                        break

                    for item in json_obj['response']:
                        craw_url = 'https://v2.myktoon.com/web/works/viewer.kt?timesseq='+str(item['timesseq'])
                        title_num = item['timestitle'].split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'myktoon',
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

    print("myktoon 크롤링 시작")
    startCrawling()
    print("myktoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
