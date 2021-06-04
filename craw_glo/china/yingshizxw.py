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
    while check:
        i = i+1
        if i == 30:
            break
        if site == '1':
            if i == 1:
                link = 'https://www.yingshizxw.com/tv/hanju/index.html'
                r = requests.get(link)
            else:
                link = 'https://www.yingshizxw.com/tv/hanju/index'
                link2 = '.html'
                r = requests.get(link+str(i)+link2)
        else:
            link = 'https://www.yingshizxw.com/search.php?page='
            link2 = '&searchtype=5&tid=3&area=韩国'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'title')

        try:
            for item in div:
                url = 'https://www.yingshizxw.com/'+item.find('a')['href']
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
                div = soup.find('div', id='playlist').find_all('div', 'panel')

                for item in div:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'https://www.yingshizxw.com/'+item.find('a')['href']
                        title = titleSub + '_' + item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'yingshizxw',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
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

    print("yingshizxw 크롤링 시작")
    site = ['1','2']
    for s in site:
        startCrawling(s)
    print("yingshizxw 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
