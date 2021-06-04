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
    link = 'https://dramafeveronline.com/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'post-container').find_all('div', 'post-box')

        try:
            for item in div:
                url = item.find('h5').find('a')['href']
                titleSub = item.find('h5').find('a').text.strip()
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
                if soup.find('iframe', 'wpve-iframe'):
                    origin_url = soup.find('iframe', 'wpve-iframe')['data-lazy-src']
                    if origin_url.find('https:') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1].split('.')[0]
                    if origin_osp.find('www.') != -1:
                        origin_osp = origin_osp.split('www.')[1]
                    elif origin_osp.find('www1.') != -1:
                        origin_osp = origin_osp.split('www1.')[1]
                else:
                    origin_url = ''
                    origin_osp = ''

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'dramafeveronline',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'indonesia',
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

    print("dramafeveronline 크롤링 시작")
    startCrawling()
    print("dramafeveronline 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
