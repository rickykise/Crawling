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
    link = "https://madooseries.com/cate/?pn="
    link2 = "&type=%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'col-md-12 well').find_all('div', 'col-md-3')

        try:
            for item in div:
                url = item.find('a')['href']
                titleDiv = item.find('div', 'caption')
                title1 = titleDiv.find_all('p')[0].text.strip()
                if title1.find('(') != -1:
                    title1 = title1.split('(')[0]
                title2 = titleDiv.find_all('p')[1].text.strip()
                if title2.find('(') != -1:
                    title2 = title2.split('(')[0]
                titleSub = title1+title2
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
                div2 = soup.find_all('div', 'container-fluid')[1].find_all('div', 'well-fluid')[1]
                sub = div2.find_all('h5')
                for p in sub:
                    host_url = p.find('a')['href']
                    title = p.find('a').text.strip()
                    title_null = titleNull(title)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # host_cnt = len(soup.find('ul', 'nav-tabs').find_all('li'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'madooseries',
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

    print("madooseries 크롤링 시작")
    startCrawling()
    print("madooseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
