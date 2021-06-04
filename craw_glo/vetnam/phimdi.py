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
    link = 'https://phimdi.com/content/search?t=ft&nt=KR&p='
    while check:
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find_all('a', 'movie-item')
        i = i+1

        try:
            for item in sub:
                url = item['href']
                titleSub1 = item.find('div', 'pl-carousel-content').find('h6').text.strip()
                titleSub2 = item.find('div', 'pl-carousel-content').find('p').text.strip()
                if titleSub2.find('(20') != -1:
                    titleSub2 = titleSub2.split('(')[0].strip()
                if titleSub1 != titleSub2:
                    titleSub = titleSub1+' '+titleSub2
                else:
                    titleSub = titleSub1
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
                sub = soup.find_all('a','movie-eps-item')

                for item in sub:
                    host_url = item['href']
                    title = titleSub + '_' + item['title']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'phimdi',
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

    print("phimdi 크롤링 시작")
    startCrawling()
    print("phimdi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
