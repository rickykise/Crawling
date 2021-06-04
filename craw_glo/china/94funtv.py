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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = site[0]
    with requests.Session() as s:
        while check:
            i = i+1
            if i == site[1]:
                break

            r = requests.get(link.format(str(i)))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find_all('li', 'fed-list-item')

            try:
                for item in li:
                    url = 'https://tw.94funtv.com'+item.find('a', 'fed-list-title')['href']
                    titleSub = item.find('a', 'fed-list-title').text.strip()
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
                    ul = soup.find('div','fed-drop-boxs').find_all('ul', 'fed-part-rows')

                    for item in ul:
                        sub = item.find_all('a','fed-btns-info')
                        for item in sub:
                            host_url = 'https://tw.94funtv.com'+item['href']
                            title = titleSub+'_'+item.text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : '94funtv',
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
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("94funtv 크롤링 시작")
    site = [['https://tw.94funtv.com/vod/show/id/15/page/{}.html',30],['https://tw.94funtv.com/vod/show/area/%E9%9F%93%E5%9C%8B/id/{}.html',17]]
    for item in site:
        startCrawling(item)
    print("94funtv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
