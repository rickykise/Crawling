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
    link = 'https://www.133133.tv/?li='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'vi_list').find_all('li')

        try:
            for item in li:
                url = item.find_all('a')[1]['href']
                titleSub = item.find_all('a')[1].text.strip()
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
                li = soup.find('div', 'list').find_all('li')

                for item in li:
                    host_url = 'https://www.133133.tv'+item.find('a')['href']
                    title_num = item.find('a').text.strip()
                    title = titleSub+'_'+title_num
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': '',
                        'cnt_osp' : '133133',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
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

    print("133133 크롤링 시작")
    site = ['drama', 'variety']
    for s in site:
        startCrawling(s)
    print("133133 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
