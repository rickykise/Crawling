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
    link = 'http://www.pengwei168.com/xkshow/{}-%E9%9F%A9%E5%9B%BD---%E9%9F%A9%E8%AF%AD----{}---.html'
    while check:
        i = i+1
        if i == site[1]:
            break
        r = requests.get(link.format(str(i), site[0]))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        sub = soup.find_all('a',  'stui-vodlist__thumb')

        try:
            for item in sub:
                url = 'http://www.pengwei168.com'+item['href']
                titleSub = item['title']
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
                url2 = 'http://www.pengwei168.com'+soup.find('div', 'play-btn').find('a', 'btn-primary')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find('div', 'tab-content').find_all('li')

                for item in li:
                    host_url = 'http://www.pengwei168.com'+item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'pengwei168',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("pengwei168 크롤링 시작")
    site = [['15', 21]]
    for s in site:
        startCrawling(s)
    print("pengwei168 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
