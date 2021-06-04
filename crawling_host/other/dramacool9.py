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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(url, keyItem):
    url = url;cnt_id = keyItem[0];cnt_osp = keyItem[1];cnt_title = keyItem[2];cnt_nat = keyItem[3];cnt_keyword = ''

    try:
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', id='all-episodes').find('ul', 'list').find_all('li')

        for item in li:
            host_url = item.find('a')['href']
            title = item.find('a')['title']
            title_null = titleNull(title)

            r = requests.get(host_url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('div', 'serverslist'):
                origin_url = soup.find('div', 'serverslist')['data-server']
                origin_osp = origin_url.split('//')[1].split('.')[0]
                if origin_osp.find('www') != -1:
                    origin_osp = origin_osp.split('www.')[1]
            else:
                origin_url = ''
                origin_osp = ''

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'dramacool9',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'other',
                'cnt_writer': '',
                'origin_url': origin_url,
                'origin_osp': origin_osp
            }
            # print(data)
            # print("=================================")

            dbResult = insertALL(data)
    except:
        pass

    dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("dramacool9 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("dramacool9 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
