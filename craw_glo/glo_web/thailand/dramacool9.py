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

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.dramacool9.co/category/'+site+'/page/'
    link2 = '/?country=korean'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'box').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                title = item.find('a')['title']
                if title.find('(') != -1:
                    title = title.split('(')[0].strip()
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

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
                        'cnt_nat': 'thailand',
                        'cnt_writer': '',
                        'origin_url': origin_url,
                        'origin_osp': origin_osp
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dramacool9 크롤링 시작")
    site = ['drama','movies']
    for s in site:
        startCrawling(s)
    print("dramacool9 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
