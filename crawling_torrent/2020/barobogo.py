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
    link = 'http://tv.barobogo.live/bbs/search.php?sfl=wr_subject%7C%7Cwr_content&stx='+key+'&sop=and&gr_id=&srows=10&onetable=&page='
    while check:
        i = i+1
        if i == 10:
            break
        r = requests.get(link+str(i))

        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('p', 'search-none'):
            break
        div = soup.find('div', 'search-media').find_all('div', 'media')

        try:
            for item in div:
                title = item.find('div', 'media-heading').find('a').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                keyCheck = checkTitle(title_null, keywordCh)
                if keyCheck == None:
                    continue

                url = 'http://tv.barobogo.live/bbs/'+item.find('div', 'media-heading').find('a')['href'].split('./')[1]
                cnt_num = url.split('wr_id=')[1]

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'barobogo',
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

    print("barobogo 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("barobogo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
