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
    while check:
        i = i+1
        if i == 30:
            break
        if site == '1':
            link = 'http://icdrama.video/browse/korean/dramas/all/all/all/0/'+str(i)
            r = requests.get(link)
        else:
            link = 'http://icdrama.video/browse/korean/tvshow/all/all/all/0/1'
            r = requests.get(link)
            i = 29
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'v-grid')

        try:
            for item in div:
                url = 'http://icdrama.video'+item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'list-eps')

                for item in div:
                    host_url = 'http://icdrama.video'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'icdrama',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("icdrama 크롤링 시작")
    site = ['1','2']
    for s in site:
        startCrawling(s)
    print("icdrama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
