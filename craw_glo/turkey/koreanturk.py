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
    link = 'https://www.koreanturk.com/bolumler/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', 'panel-body').find_all('a', 'izlenmedi')

        try:
            for item in sub:
                url = item['href']
                titleSub1 = item.find('span').text.strip()
                titleSub2 = item.find('h2', 'standart-title').text.replace('\n', '').split(titleSub1)[1]
                titleSub = titleSub1+' '+titleSub2
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

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'koreanturk',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'turkey',
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)

                if soup.find('table', 'table-striped'):
                    tr = soup.find('table', 'table-striped').find('tbody').find_all('td','banacak')

                    for item in tr:
                        host_url = item.find('a')['href']
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'koreanturk',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'turkey',
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

    print("koreanturk 크롤링 시작")
    startCrawling()
    print("koreanturk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
