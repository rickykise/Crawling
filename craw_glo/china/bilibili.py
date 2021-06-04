import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': '_uuid=0BDAE319-FA31-2D45-8344-C08F7ECB1A2B25864infoc; buvid3=5EFCDA81-FF4A-4044-9CB5-8341A48CA4F9155829infoc; LIVE_BUVID=AUTO7815712060247214',
    'Host': 'search.bilibili.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://search.bilibili.com/all?keyword='+keyword+'&page='
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 30:
                break
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            sub = soup.find_all('a', 'img-anchor')

            try:
                for item in sub:
                    url = item['href']
                    if url.find('http') == -1:
                        url = 'https:'+item['href']
                    title = item['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bilibili',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': '',
                        'cnt_keyword_nat': k_nat
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getKey = getKeywordCH()

    print("bilibili 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("bilibili 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
