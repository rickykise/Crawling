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
    link = 'https://www.97hanju.com/list/'+site+'/index-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            link = 'https://www.97hanju.com/list/'+site+'/index.html'
            r = requests.get(link)
        else:
            link = 'https://www.97hanju.com/list/'+site+'/index-'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        dl = soup.find_all('dl', 'list')

        try:
            for item in dl:
                url = 'https://www.97hanju.com'+item.find('dd', 'title').find('a')['href']
                titleSub = item.find('dd', 'title').find('a')['title']
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
                ul = soup.find_all('ul', 'play-list')

                for item in ul:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'https://www.97hanju.com'+item.find('a')['href']
                        title = titleSub + item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '97hanju',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
                            'cnt_writer': '',
                            'origin_url': '',
                            'origin_osp': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("97hanju 크롤링 시작")
    site = ['dianshiju', 'zongyi', 'dianying']
    for s in site:
        startCrawling(s)
    print("97hanju 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
