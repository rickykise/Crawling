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
    link = 'http://www.mlpdy.com/list/24-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        if site == '4':
            link = 'http://www.mlpdy.com/vod-type-id-4-wd--letter--year--area-%E9%9F%A9%E5%9B%BD-order--p-'
            link2 = '.html'
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'filmlist').find_all('li')

        try:
            for item in li:
                url = item.find('div', 'v_title').find('a')['href']
                if url.find('mlpdy') == -1:
                    url = 'http://www.mlpdy.com'+url
                titleSub = item.find('div', 'v_title').find('a').text.strip()
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
                sub = soup.find('div', 'clearfix mb40').find_all('a', 'list-p-button')

                for item in sub:
                    host_url = item['href']
                    if host_url.find('mlpdy') == -1:
                        host_url = 'http://www.mlpdy.com'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)
                    host_cnt = 1

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'mlpdy',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': host_cnt,
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
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

    print("mlpdy 크롤링 시작")
    site = ['24', '4']
    for s in site:
        startCrawling(s)
    print("mlpdy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
