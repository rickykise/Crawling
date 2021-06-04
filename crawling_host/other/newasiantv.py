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
        url2 = 'https://wwv.newasiantv.tv'+soup.find('a', 'watch_button')['href']

        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'episode_list').find_all('li')

        for item in li:
            host_url = 'https://wwv.newasiantv.tv'+item.find('a')['href']
            titleNum = item.find('a').text.strip()
            if titleNum.find('RAW') != -1:
                titleNum = titleNum.split('RAW')[0].strip()
            title = cnt_title+'_'+titleNum
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'newasiantv',
                'cnt_title': title,
                'cnt_title_null': title_null,
                'host_url' : host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'other',
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

    print("newasiantv 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("newasiantv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
