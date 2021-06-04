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
    link = 'https://dgb-toon3.site/?view=weekly&week='
    val = ['sun','mon','tue','wed','thu','fri','sat','10']
    for v in val:
        r = requests.get(link+v)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'list-container').find_all('div', 'section-item-title')

        try:
            for item in div:
                url = 'https://dgb-toon3.site'+item.find('a')['href']
                title = item.find('a')['alt']
                title_check = titleNull(title)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                td = soup.find('table', 'web_list').find_all('td', 'episode__index')

                for item in td:
                    craw_url = 'https://dgb-toon3.site'+item['data-role']
                    title_numCh = titleNull(item['alt'])
                    title_num = title_numCh.replace(title_check, '').split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'dgb-toon3',
                        'craw_domain': 'site',
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

    print("dgb-toon3 크롤링 시작")
    startCrawling()
    print("dgb-toon3 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
