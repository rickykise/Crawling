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
    link = 'https://replaytv1.com/search/index?keywords='+key
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('ul', 'main_bn')[1].find_all('li')
        if len(li) <= 1:
            break

        try:
            for item in li:
                title = item.find_all('a', 'tit')[1].text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                keyCheck = checkTitle(title_null, keywordCh)
                if keyCheck == None:
                    continue

                url = 'https://replaytv1.com'+item.find_all('a', 'tit')[1]['href']
                cnt_num = url.split('video/')[1]

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'replaytv1',
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

    print("replaytv1 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("replaytv1 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
