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
    i = 0;a = 1;check = True
    link = 'http://www.dramagalaxy.tv/drama-shows'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        table = soup.find_all('table', 'series_index')

        try:
            for item in table:
                if a == 26:
                    a = 1
                    break
                tr = item.find_all('tr')
                for item in tr:
                    url = item.find('a')['href']
                    titleSub = item.find('a').text.strip()
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
                    div = soup.find('div', id='videos')
                    li = div.find('ul').find_all('li')

                    for item in li:
                        host_url = item.find('a')['href']
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)

                        # r = requests.get(host_url)
                        # c = r.content
                        # soup = BeautifulSoup(c,"html.parser")
                        # host_cnt = len(soup.find_all('div', 'vmargin'))

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'dramagalaxy',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'philippines',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
                a += 1
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dramagalaxy 크롤링 시작")
    startCrawling()
    print("dramagalaxy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
