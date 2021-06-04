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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = "https://video2free.com/category/ซีรีส์เกาหลี/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'cactus-sub-wrap').find_all('article', 'cactus-post-item hentry')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('EP') != -1:
                    titleSub = item.find('a')['title'].split('EP')[0].strip()
                cnt_num = item.find('a', 'btn')['data-id']
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
                div = soup.find('div', 'content-epls').find_all('a')
                for item in div:
                    host_url = item['href']
                    title_num = item.text.strip()
                    title = titleSub+'_'+title_num
                    title_null = titleNull(title)
                    # host_cnt = len(soup.find('div', 'series-content').find_all('div', 'series-content-row'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'video2free',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
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

    print("video2free 크롤링 시작")
    startCrawling()
    print("video2free 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
