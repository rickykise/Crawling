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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'http://www.rehuo.org/o/{}--------{}---.html'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == site[1]:
                break
            r = s.get(link.format(site[0],str(i)))
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            li = soup.find_all('li',  'fed-list-item')

            try:
                for item in li:
                    url = 'http://www.rehuo.org'+item.find('a')['href']
                    titleSub = item.find('a',  'fed-list-title').text.strip()
                    title_check = titleNull(titleSub)

                    
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check,  getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c, "html.parser")
                    ul = soup.find('div',  'fed-drop-btms').find_all('ul','fed-part-rows')
                    for item in ul:
                        li = item.find_all('li','fed-col-lg1')
                        for item in li:
                            host_url = 'http://www.rehuo.org'+item.find('a','fed-btns-info')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp': 'rehuo.org',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url': host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'china',
                                'cnt_writer': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
            except Exception as e:
                print(e)
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("rehuo.org 크롤링 시작")
    page = [['20',15],['3',8]]
    for target in page:
        startCrawling(target)
    print("rehuo.org 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
