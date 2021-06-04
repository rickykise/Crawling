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

def startCrawling():
    i = 0;check = True
    link = 'http://seriesubthai.cc/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5/index'
    link2 = '.htm'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            i = str('')
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if i == '':
            i = int(1)
        td = soup.find('div', 'index-tj').find_all('li')

        try:
            for item in td:
                url = 'http://seriesubthai.cc' + item.find('a')['href']
                titleSub = item.find('div', 'text').find('p', 'name').text.strip()
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
                li = soup.find('ul', 'urlli').find_all('li')

                for item in li:
                    host_url = 'http://seriesubthai.cc'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # host_cnt = len(soup.find('div', 'pfrom').find_all('li', id=re.compile("tab+")))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'seriesubthai',
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

    print("seriesubthai 크롤링 시작")
    startCrawling()
    print("seriesubthai 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
