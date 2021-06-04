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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://www2.ondramanice.tv/list-all-drama'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'drama_list_body').find_all('div', 'list_items')
        try:
            for item in div:
                li = item.find('ul').find_all('li')
                for item in li:
                    url = 'https://www2.ondramanice.tv' + item.find('a')['href']
                    titleSub = item.find('a').text.strip()
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
                    li = soup.find('ul', 'list_episode').find_all('li')

                    for item in li:
                        host_url = 'https://www2.ondramanice.tv' + item.find('a')['href']
                        title = titleSub + item.find('a').text.strip()
                        title_null = titleNull(title)

                        # r = requests.get(host_url)
                        # c = r.content
                        # soup = BeautifulSoup(c,"html.parser")
                        # host_cnt = len(soup.find('div', 'anime_muti_link').find_all('li'))

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'ondramanice',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'other',
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

    print("ondramanice 크롤링 시작")
    startCrawling()
    print("ondramanice 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
