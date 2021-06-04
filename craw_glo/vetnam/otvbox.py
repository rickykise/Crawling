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
    link = 'https://www.otvbox.com/quoc-gia/han-quoc/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('div', 'drama-item')

        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a').find('img')['alt']
                if titleSub.find('Tập') != -1:
                    titleSub = titleSub.split('Tập')[1].strip()
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
                url2 = soup.find('a', 'btn')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'listep').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    titleNum = item.find('a').text.strip()
                    if titleNum.find('Tập') != -1:
                        titleNum = titleNum.split('Tập')[1].strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # host_cnt = len(soup.find('div', 'list_episodes').find_all('div', 'server_item'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'otvbox',
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

    print("otvbox 크롤링 시작")
    startCrawling()
    print("otvbox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
