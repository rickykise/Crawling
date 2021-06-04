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

    while check:
        i = i+1
        if i == 2:
            break
        link = 'https://www.rudals1.net/검색:'+keyword
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'row')
        text = str(div)
        if text.find('검색결과가 없습니다') != -1:
            break
        try:
            title = div.find('a')['title']
            title_null = titleNull(title)
            # 키워드 체크
            if title_null.find(keywordCh) == -1:
                break
            url = 'https://www.rudals1.net'+div.find('a')['href']
            cnt_num = datetime.datetime.now().strftime('%y%m%d%H%M%S')

            data = {
                'Cnt_num' : cnt_num,
                'Cnt_osp' : 'rudals1',
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

    print("rudals1 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("rudals1 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
