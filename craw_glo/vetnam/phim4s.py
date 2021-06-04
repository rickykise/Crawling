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
    link = 'http://phim4s.net/country/han-quoc'
    while check:
        if i == 96:
            break
        if i == 0:
            r = requests.get(link)
        else:
            r = requests.get(link+'/'+str(i)+'.html')
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        i = i+24
        div = soup.find_all('div', 'movie-title')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                print(url)
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                print(soup)
                sub = soup.find('div', 'season').find_all('a')

                for item in sub:
                    host_url = item['href']
                    titleNum = item.text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'phim4s',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phim4s 크롤링 시작")
    startCrawling()
    print("phim4s 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
