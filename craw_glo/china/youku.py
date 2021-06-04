import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
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
    i = 0;a = 1;check = True
    link = 'https://list.youku.com/category/page?c='+site+'&a=%E9%9F%A9%E5%9B%BD&type=show&p='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        textJ = str(soup)
        jsonString = json.loads(textJ)
        text = str(jsonString)

        try:
            for item in text:
                url = 'https://v.youku.com/v_show/id_'+text.split("'videoId': '")[a].split("', '")[0]
                titleSub = text.split("'title': '")[a].split("', '")[0]
                title_check = titleNull(titleSub)
                a = a+1
                if a == 85:
                    a = 1
                    break
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
                div = soup.find_all('div', 'item item-num')

                for item in div:
                    host_url = item.find('a')['href']
                    if host_url.find('https') == -1:
                        host_url = 'https:'+host_url
                    title = titleSub+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'youku',
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

    print("youku 크롤링 시작")
    site = ['97&s=1&d=1','85','96']
    for s in site:
        startCrawling(s)
    print("youku 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
