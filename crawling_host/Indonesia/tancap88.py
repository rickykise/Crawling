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
        div = soup.find('div', 'episodes__inner').find_all('div', re.compile("post-+"))

        for item in div:
            host_url = item.find('a', 'episode__link')['href']
            title = item.find('h3', 'episode__title').text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'tancap88',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'indonesia',
                'cnt_writer': ''
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

    print("tancap88 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("tancap88 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
