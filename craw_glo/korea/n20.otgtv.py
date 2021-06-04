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
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'https://n20.otgtv.top/show/'+site+'/section/new/p'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('table', 'div-table').find('tbody').find_all('tr')

        # try:
        for item in tr:
            url = item.find('a')['href']
            title = item.find('a').text.strip()
            title_null = titleNull(title)
            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_null, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']
            keyCheck2 = checkTitle2(title_null, getKey)
            if keyCheck2['m'] == None:
                continue

            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find_all('button', 'baseLinkButton')

            for item in sub:
                host_url = item['onclick'].split("Window('")[1].split("',")[0]
                if host_url.find('show/drama') != -1:
                    continue

                origin_url = host_url

                if origin_url.find('https') == -1:
                    origin_url = 'https:'+origin_url
                origin_osp = origin_url.split('//')[1]
                if origin_osp.find('www') != -1:
                    origin_osp = origin_osp.split('www.')[1].split('.')[0]
                else:
                    origin_osp = origin_osp.split('.')[0]

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'n20.otgtv',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'southkorea',
                    'cnt_writer': '',
                    'origin_url': origin_url,
                    'origin_osp': origin_osp
                }
                print(data)
                print("=================================")

        #             dbResult = insertALL(data)
        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("n20.otgtv 크롤링 시작")
    site = ['drama', 'ent']
    for s in site:
        startCrawling(s)
    print("n20.otgtv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
