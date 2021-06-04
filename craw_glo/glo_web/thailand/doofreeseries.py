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
    i = 0;check = True
    link = "http://www.doofreeseries.com/category/ดูซีรี่ย์เกาหลี/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'td-ss-main-content').find_all('div', 'td-module-thumb')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('EP') != -1:
                    titleSub = item.find('a')['title'].split('EP')[0].strip()
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
                sub = soup.find_all('p', style='text-align: center;')
                for item in sub:
                    if item.find('a'):
                        host_url = item.find('a')['href']
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)

                        # r = requests.get(host_url)
                        # c = r.content
                        # soup = BeautifulSoup(c,"html.parser")
                        # host_cnt = len(soup.find('div', 'td-ss-main-content').find_all('h2', 'tabtitle'))

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'doofreeseries',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'thailand',
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

    print("doofreeseries 크롤링 시작")
    startCrawling()
    print("doofreeseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")