import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

def startCrawling(key):
    keyword = key
    keywordCh = keyword.replace(' ', '')
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'http://www.goratv.com/search/?skeyword='+keyword+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'media')
        if len(div) <= 1:
            break
        try:
            for item in div:
                title = item.find('a')['title']
                title_null = titleNull(title)
                # 키워드 체크
                if title_null.find(keywordCh) == -1:
                    continue
                url = item.find('a')['href']
                cnt_num = url.split('post/')[1].strip()

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'goratv',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': '',
                    'Cnt_writer' : '',
                    'Cnt_vol' : '',
                    'Cnt_fname' : '',
                    'Cnt_chk': 0
                }
                # print(data)
                # print('=============================================')

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("goratv 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("goratv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
