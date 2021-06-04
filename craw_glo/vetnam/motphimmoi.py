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
    'Accept': 'text/html,  application/xhtml+xml,  image/jxr,  */*', 
    'Accept-Encoding': 'gzip,  deflate', 
    'Accept-Language': 'ko-KR', 
    'Connection': 'Keep-Alive', 
    'Cookie': '__test; __cfduid=d97bd8cf4a1bde533018dc66c35bbe5291618379363; vDDoS=3696a20614876aa7df4f0c6b1a1300a9; PHPSESSID=vhaapc2dnb85n6mhe24kmtcn2k; _ga=GA1.2.1688929972.1618379365; _gid=GA1.2.1238403617.1618379365; __test; __PPU___PPU_SESSION_URL=%2F; adsphimmoi=Ads%20PhimMoi', 
    'Host': 'motphimmoi.net', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 1;check = True
    link = 'http://motphimmoi.net/country/han-quoc/page/'
    while check:
        i = i+1
        if i == 29:
            break
        if i == 1:
            href = 'http://motphimmoi.net/country/han-quoc/'
        else:
            href = link+str(i)+'/'
        r = requests.get(href,headers=headers)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        article = soup.find('div',  'halim_box').find_all('article')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url,headers=headers)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                url2 = soup.find('a', 'watch-movie')['href']

                r = requests.get(url2,headers=headers)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                ul = soup.find_all('ul',  'halim-list-eps')

                for item1 in ul:
                    li = item1.find_all('li','halim-episode')
                    for item2 in li:
                        host_url = item2.find('a')['href']
                        title = titleSub+'_'+item2.find('span').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp': 'motphimmoi',
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
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("motphimmoi 크롤링 시작")
    startCrawling()
    print("motphimmoi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
