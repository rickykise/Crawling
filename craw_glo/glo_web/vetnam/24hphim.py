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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://24hphim.com/quoc-gia/kr/trang-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'list-film').find_all('div', 'item')

        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
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
                url2 = soup.find('div', 'watch').find('a')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'episodes').find('ul').find_all('li')

                for item in li:
                    host_url = 'https://24hphim.com'+item.find('a')['href']
                    cnt_num = item.find('a')['id']
                    titleNum = item.find('a').text.strip()
                    if titleNum.find('Full') != -1:
                        title = titleSub
                    else:
                        title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    # r = requests.get(url2)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # host_cnt = len(soup.find('div', 'block servers').find_all('div', 'name'))

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '24hphim',
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

    print("24hphim 크롤링 시작")
    startCrawling()
    print("24hphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
