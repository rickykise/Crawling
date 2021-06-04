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

def startCrawling():
    i = 0;check = True
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            r = requests.get('https://meijushijie.com/meijushijie/2.html')
        else:
            link = 'https://meijushijie.com/meijushijie/2-'
            link2 = '.html'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'u-movie')

        try:
            for item in article:
                url = 'https://meijushijie.com'+item.find('a')['href']
                titleSub = item.find('a')['title']
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
                div = soup.find_all('div', 'playlist')

                for item in div:
                    li = item.find_all('li')

                    for item in li:
                        host_url = 'https://meijushijie.com'+item.find('a')['href']
                        if host_url.find('play') == -1:
                            continue
                        title = titleSub+'_'+item.find('a')['title']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'meijushijie',
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

    print("meijushijie 크롤링 시작")
    startCrawling()
    print("meijushijie 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
