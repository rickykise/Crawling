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
    a = 1
    link = 'https://toptoon.com/weekly'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    text_area = text.split('jsonFileUrl')[1].split('arrayMenuNames')[0].replace('\\', '')


    for i in text:
        try:
            host_url_ch = text_area.split('"https')[a].split('",')[0].strip()
            host_url = 'https'+host_url_ch
            if host_url.find('"]') != -1:
                host_url = host_url.split('"]')[0].strip()
            a = a+1

            print(host_url)
            r = requests.get(host_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            json_obj = json.loads(text)

            for item in json_obj['non_adult']:
                url = 'https://toptoon.com'+str(item).split("comicsListUrl': '")[1].split("',")[0].strip()
                title = str(item).split("'title': '")[1].split("'")[0].strip()

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                tr = soup.find_all('tr', 'episode_tr')

                for item in tr:
                    craw_url = url.replace('ep_list', 'ep_view')+'/'+item['data-episode-id']
                    title_num = item['data-episode-id']

                    data = {
                        'craw_osp_id': 'toptoon',
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

    print("toptoon 크롤링 시작")
    startCrawling()
    print("toptoon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
