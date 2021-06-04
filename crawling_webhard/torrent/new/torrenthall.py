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
    keyword = urllib.parse.unquote(key)
    keywordCh = key.replace(' ', '')
    print('키워드: '+key)
    i = 0;check = True
    link = 'https://torrenthall.com/search?skeyword='+keyword
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li', 'list-item')
        if len(li) <= 1:
            break
        try:
            for item in li:
                title = item.find('a', 'subject')['title']
                title_null = titleNull(title)
                # 키워드 체크
                if title_null.find(keywordCh) == -1:
                    continue
                url = item.find('a')['href']
                cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'torrenthall',
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

    print("torrenthall 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("torrenthall 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
