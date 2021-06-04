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

def startCrawling(site):
    i = 0;check = True
    link = 'https://list.iqiyi.com/www/'+site+'-------------11-'
    link2 = '-1-iqiyi--.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        print(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('ul', 'qy-mod-ul').find_all('li', 'qy-mod-li')
        # try:
        for item in div:
            url = item.find('div', 'title-wrap').find('a')['href']
            if url.find('https') == -1:
                url = 'https:'+url
            titleSub = item.find('div', 'title-wrap').find('a')['title']
            title_check = titleNull(titleSub)
            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            if site == '1/4':
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'iqiyi',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
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
            elif site == '2/17':
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('p', 'site-piclist_info_title')

                for item in div:
                    host_url = item.find('a')['href']
                    if host_url.find('www.iqiyi.com') == -1:
                        continue
                    if host_url.find('https') == -1:
                        host_url = 'https:'+host_url
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'iqiyi',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
            else:
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'piclist-horizontal-details')

                for item in div:
                    host_url = item.find('a')['href']
                    if host_url.find('www.iqiyi.com') == -1:
                        continue
                    if host_url.find('https') == -1:
                        host_url = 'https:'+host_url
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'iqiyi',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
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

    print("iqiyi 크롤링 시작")
    site = ['1/4','2/17','6/153']
    for s in site:
        startCrawling(s)
    print("iqiyi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
