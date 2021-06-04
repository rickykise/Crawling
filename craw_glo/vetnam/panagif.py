import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
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


headers = {
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,th;q=0.6,zh-CN;q=0.5,zh;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'Cookie': 'PHPSESSID=8r4odpmcqqbk5s3rlgonev5gv6',
    'Referer': 'http://panagif.com/eo-ymj-qtan/umnr-gt-mtas-ymasm/'
}


def startCrawling():
    i = 0;check = True
    link = 'http://panagif.com/the-loai/phim-bo-hoan-thanh/trang-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 11:
            break
        r = requests.get(link+str(i)+link2,headers=headers)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('ul',  'list-movie').find_all('li',  'movie-item')
        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url,headers=headers)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', id="btn-film-watch")['href']

                r = requests.get(url2,headers=headers)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find('ul',  'list-episode').find_all('li',  'episode')
                print(len(li))

                for item in li:
                    host_url = 'http://panagif.com'+item.find('a')['href']
                    titleNum = item.find('a').text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'panagif',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("panagif 크롤링 시작")
    startCrawling()
    print("panagif 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
