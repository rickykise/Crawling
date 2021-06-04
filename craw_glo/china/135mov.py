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
    link = 'http://www.135mov.com/list-select-id-'+site+'-type--area-韓國-year--star--state--order-hits-p-'
    link2 = '.html'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = s.get(link+str(i)+link2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find_all('li', 'stui-vodlist__item')

            try:
                for item in li:
                    url = 'http://135mov.com'+item.find('a')['href']
                    titleSub = item.find('h4').text.strip()
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
                    ul = soup.find_all('ul', 'stui-content__playlist')

                    for item in ul:
                        li = item.find_all('li')
                        for item in li:
                            host_url = 'http://135mov.com'+item.find('a')['href']
                            title = titleSub+'_'+item.find('a').text.strip()
                            if title.find('SP') != -1:
                                continue
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : '135mov',
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

    print("135mov 크롤링 시작")
    site = ['2', '4']
    for s in site:
        startCrawling(s)
    print("135mov 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
