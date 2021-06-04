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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Host': 'www.paojiaoys.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'http://www.paojiaoys.com/'+site+'/rihan/page/'
    while check:
        i = i+1
        if i == 30:
            break
        print(link+str(i))
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(soup)
        li = soup.find_all('li', 'item')

        # try:
        for item in li:
            url = 'http://www.paojiaoys.com'+item.find('a')['href']
            titleSub = item.find('a')['title']
            title_check = titleNull(titleSub)
            print(url)
            print(titleSub)
            print("=================================")
            # 키워드 체크
            # getKey = getKeyword()
            # keyCheck = checkTitle(title_check, getKey)
            # if keyCheck['m'] == None:
            #     continue
            # cnt_id = keyCheck['i']
            # cnt_keyword = keyCheck['k']
            #
            # r = requests.get(url)
            # c = r.content
            # soup = BeautifulSoup(c,"html.parser")
            # ul = soup.find_all('ul', 'play-list')
            #
            # for item in ul:
            #     li = item.find_all('li')
            #     for item in li:
            #         host_url = 'https://www.97hanju.com'+item.find('a')['href']
            #         title = titleSub + item.find('a').text.strip()
            #         title_null = titleNull(title)
            #
            #         data = {
            #             'cnt_id': cnt_id,
            #             'cnt_osp' : 'paojiaoys',
            #             'cnt_title': title,
            #             'cnt_title_null': title_null,
            #             'host_url' : host_url,
            #             'host_cnt': '1',
            #             'site_url': url,
            #             'cnt_cp_id': 'sbscp',
            #             'cnt_keyword': cnt_keyword,
            #             'cnt_nat': 'china',
            #             'cnt_writer': '',
            #             'origin_url': '',
            #             'origin_osp': ''
            #         }
            #         print(data)
            #         print("=================================")

                        # dbResult = insertALL(data)
        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("paojiaoys 크롤링 시작")
    site = ['lianxuju', 'zongyi']
    for s in site:
        startCrawling(s)
    print("paojiaoys 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
