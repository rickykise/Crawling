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
    link = 'https://xemphim1.com/'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div','panel-group').find_all('div','menu-panel')
    for item in div:
        try:
            url = 'https://xemphim1.com'+item.find('a')['href']
            titleSub = item['heading']
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
            url2 = 'https://xemphim1.com'+soup.find('a', 'yt-ui-ellipsis')['href']

            r = requests.get(url2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('ul','listep').find_all('li')

            for item in li:
                title = titleSub + '_' + item.find('a').text.strip()
                title_null = titleNull(title)
                host_url = 'https://xemphim1.com/'+item.find('a')['href']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'xemphim1',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : host_url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vietnam',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except Exception as e:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xemphim1 크롤링 시작")
    startCrawling()
    print("xemphim1 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
