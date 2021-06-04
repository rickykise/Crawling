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
    link = 'https://www.meiku.live/Korea/Drama/'+site
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'row').find_all('div', 'views-field')

        for item in div:
            try:
                url = 'https://www.meiku.live'+item.find('h4').find('a')['href']
                titleSub = item.find('h4').find('a').text.strip()
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
                div = soup.find('div', 'view-content').find_all('div', 'views-row')

                for item in div:
                    host_url = 'https://www.meiku.live'+item.find('a')['href']
                    title = item.find('a').text.strip()
                    if title.find('Ep') != -1:
                        title = titleSub+'_'+title.split('Ep')[1]
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    host_cnt = len(soup.find_all('iframe'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'meiku',
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

                    dbResult = insertALL(data)
            except:
                continue


if __name__=='__main__':
    start_time = time.time()

    print("meiku 크롤링 시작")
    site = ['2019', '2018', '2017', '2016']
    for s in site:
        startCrawling(s)
    print("meiku 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
