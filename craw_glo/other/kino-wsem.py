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
    link = 'https://kino-wsem.ru/page/'
    while check:
        i = i+1
        if i == 50:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        table = soup.find('div', 'e-news').find_all('table', 'e-news')

        try:
            for item in table:
                url = item.find('a')['href']
                titleSub1 = item.find('span', 'e-vid').text.strip()
                titleSub2 = item.find_all('span', 'e-vid')[1].text.strip()
                titleSub = item.text.split(titleSub1)[1].split(titleSub2)[0].replace(':', '').strip()
                if titleSub.find(' /') != -1:
                    titleSub = titleSub.split(' /')[0].strip()
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
                option = soup.find('select', 'parce_playlist').find_all('option')

                for item in option:
                    try:
                        host_url = item['value']
                        if host_url.find('http:') == -1:
                            host_url = "http:"+host_url
                        title = titleSub+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': 'cnt_id',
                            'cnt_osp' : 'kino-wsem',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': 'cnt_keyword',
                            'cnt_nat': 'other',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
                    except:
                        continue
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kino-wsem 크롤링 시작")
    startCrawling()
    print("kino-wsem 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
