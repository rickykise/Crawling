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
    link = 'http://phim14.net/quoc-gia/phim-han-quoc.'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', id='content').find('ul', 'list-film').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                h2 = item.find('div', 'info').find('h2').text.strip()
                if h2.find('(') != -1:
                    h2 = h2.split('(')[0]
                titleSub = h2 + item.find('div', 'info').find('div', 'name2').text.strip()
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
                titleEng = soup.find('div', 'alt2').find('font').text.strip()
                url2 = soup.find('div', 'phimbtn').find('a')['href']
                if titleEng.find('2019') != -1 or titleEng.find('2018') != -1 or titleEng.find('2017') != -1:
                    titleEng = titleEng.split('201')[0].strip()

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                # host_cnt = 1
                li = soup.find('ul', id='server_list').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    cnt_num = item.find('a')['id']
                    titleNum = item.find('a').text.strip()
                    if titleNum.find('-') != -1:
                        titleNum = titleNum.split('-')[0]
                    title = titleEng+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'phim14',
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

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phim14 크롤링 시작")
    startCrawling()
    print("phim14 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
