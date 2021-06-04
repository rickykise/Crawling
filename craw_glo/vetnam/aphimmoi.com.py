import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
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
    link = 'https://aphimmoi.com/country/han-quoc-0a110/{}.aspx'
    while check:
        i = i+1
        if i == 17:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div', 'boxrightmid').find_all('div', 'Form2')

        try:
            for item in div:
                url = 'https://aphimmoi.com'+item.find('a')['href']
                titleSub = item.find('p','Form2Text').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                sub = soup.find('div', 'num_film').find_all('a')
                for item in sub:
                    host_url =  'https://aphimmoi.com'+item['href']
                    title = titleSub + '_' + item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'aphimmoi.com',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")
                    
                    # dbResult = insertALL(data)

        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("aphimmoi.com 크롤링 시작")
    startCrawling()
    print("aphimmoi.com 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
