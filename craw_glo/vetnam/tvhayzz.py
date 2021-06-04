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
    link = 'https://tvhayzz.com/country/han-quoc/page/'
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        article = soup.find('div',  'halim_box').find_all('article')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', 'watch-movie')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                ul = soup.find_all('ul',  'halim-list-eps')

                for item1 in ul:
                    li = item1.find_all('li','halim-episode')
                    for item2 in li:
                        host_url = 'https://tvhayzz.com/xem-phim/'+url.replace('https://tvhayzz.com/','').replace('/','')+'-tap-'+item2.find('span')['data-episode']+'-sv-'+item2.find('span')['data-server']
                        title = titleSub+'_'+item2.find('span')['data-episode']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'tvhayzz',
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
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tvhayzz 크롤링 시작")
    startCrawling()
    print("tvhayzz 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
