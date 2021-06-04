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
    link = 'https://razorphimzz.com/phimbo/page/'
    while check:
        i = i+1
        if i == 19:
            break
        try:
            r = requests.get(link+str(i))
            c = r.text
            soup = BeautifulSoup(c, "html.parser")
            article = soup.find('div', id="archive-content").find_all('article', id=re.compile("post-+"))

            for item in article:
                url = item.find('h3').find('a')['href']
                titleSub = item.find('h3').find('a').text.strip()
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
                li = soup.find('ul', 'episodios').find_all('li',  class_=re.compile("mark-+"))

                for item in li:
                    host_url = item.find('a')['href']
                    title = titleSub+'_'+item.find('div','numerando').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'razorphimzz',
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
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            # print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("razorphimzz 크롤링 시작")
    startCrawling()
    print("razorphimzz 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
