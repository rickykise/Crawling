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

def startCrawling():
    try:
        url = 'http://www.phimtructuyenhd.com/2014/05/bac-si-xu-la-doctor-stranger-2014-tap-2.html'
        r = requests.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(soup)
        li = soup.find_all('li', 'ep')

        for item in li:
            print(item)
            # host_url = url+item.find('a')['href']
            # title = cnt_title+'_'+item.find('a').text.strip()
            # title_null = titleNull(title)
            #
            # data = {
            #     'cnt_id': cnt_id,
            #     'cnt_osp' : 'phimtructuyenhd',
            #     'cnt_title': title,
            #     'cnt_title_null': title_null,
            #     'host_url' : host_url,
            #     'host_cnt': '1',
            #     'site_url': url,
            #     'cnt_cp_id': 'sbscp',
            #     'cnt_keyword': cnt_keyword,
            #     'cnt_nat': 'vietnam',
            #     'cnt_writer': ''
            # }
            # print(data)
            print("=================================")

            # dbResult = insertALL(data)
    except:
        pass

    # dbInResult = dbUpdate(url)

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getUrl = gethost(osp_id)

    print("phimtructuyenhd 크롤링 시작")
    # for u, i in getUrl.items():
    #     startCrawling(u, i)
    startCrawling()
    print("phimtructuyenhd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
