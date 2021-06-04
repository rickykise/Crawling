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
    links = ['https://inssa01.net/bbs/search_drama.php?sfl=wr_subject%7C%7Cwr_content&stx='+key,
            'https://inssa01.net/bbs/search_enter.php?sfl=wr_subject%7C%7Cwr_content&stx='+key]

    while check:
        i = i+1
        if i == 2:
            break
        for l in links:
            r = requests.get(l)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            try:
                if soup.find('a', 'title'):
                    sub = soup.find('a', 'title')
                    title = sub.text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    keyCheck = checkTitle(title_null, keywordCh)
                    if keyCheck == None:
                        continue

                    url = sub['href']
                    cnt_num = url.split('sca=')[1]

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'inssa01',
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
                break

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("inssa01 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("inssa01 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
