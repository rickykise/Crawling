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
        url2 = url+"/watch"
        r = requests.get(url2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', id='list-eps').find_all('a')

        for item in sub:
            ep = item['onclick'].split('iframe(')[1].split(',')[0].strip()
            sv = item['onclick'].split(',')[1].split(')')[0].strip()
            host_url = url2+'/?ep='+ep+'&sv='+sv
            title = cnt_title+'_'+item.text.strip()
            title_null = titleNull(title)

            data = {
                'cnt_id': cnt_id,
                'cnt_osp' : 'studioxx1',
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

    print("studioxx1 크롤링 시작")
    for u, i in getUrl.items():
        startCrawling(u, i)
    print("studioxx1 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
