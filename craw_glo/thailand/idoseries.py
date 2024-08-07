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
    'Cookie': '__cfduid=da6440f32e43ee2942b69d0c2fa8ff12f1615772940; _ga=GA1.2.1713882003.1615772943; _gid=GA1.2.1797388692.1615772943', 
    'Host': 'idoseries.co', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}
def startCrawling():
    i = 0;check = True
    
    link = 'https://idoseries.co/genres/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5/page/{}/'
    while check:
        i = i+1
        if i == 5:
            break
        r = requests.get(link.format(str(i)),  headers=headers)
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find('div',  'listupd').find_all('article',  'bs')

        try:
            for item in div:
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

                r = requests.get(url,  headers=headers)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                li = soup.find('div',  'eplister').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    title = item.find('div','epl-title').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'idoseries',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': '',
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("idoseries 크롤링 시작")
    startCrawling()
    print("idoseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
