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

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.juji.tv/'+site+'/index-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            link = 'https://www.juji.tv/'+site+'/index.html'
            r = requests.get(link)
        else:
            link = 'https://www.juji.tv/'+site+'/index-'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'show-list').find_all('li')

        try:
            for item in li:
                url = 'https://www.juji.tv'+item.find('div', 'play-txt').find('a')['href']
                titleSub = item.find('div', 'play-txt').find('a').text.strip()
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
                li = soup.find('ul', 'play-list').find_all('li')

                for item in li:
                    host_url = 'https://www.juji.tv'+item.find('a')['href']
                    title = titleSub + item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'juji',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("juji 크롤링 시작")
    site = ['dianshiju', 'zongyi', 'dianying']
    for s in site:
        startCrawling(s)
    print("juji 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
