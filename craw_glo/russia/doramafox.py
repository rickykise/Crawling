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
    link = 'https://doramafox.ru/country/yuzhnaya-koreya/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        section = soup.find_all('section', 'post-list')

        # try:
        for item in section:
            url = item.find('a')['href']
            titleSub = item.find('a').text.strip()
            print(titleSub)
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            print(url)
            r = requests.get(url)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            print(soup)
            li = soup.find('ul', id='fox-serii').find_all('span')

            for item in li:
                span = item
                for item in span:
                    host_url = item['onclick'].split("('")[1].split("',")[0]
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'doramafox',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'russia',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                        # dbResult = insertALL(data)
        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("doramafox 크롤링 시작")
    startCrawling()
    print("doramafox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
