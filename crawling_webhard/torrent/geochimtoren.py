import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True
    link = 'https://geochimtoren.com/list.php?cate='+site+'&page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            th = soup.find('div', id='CHARTrealtime').find('tbody').find_all('th', 'title')

            try:
                for item in th:
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = 'https://geochimtoren.com'+item.find('a')['href']
                    if url.find('&page=') != -1:
                        url = url.split('&page=')[0].strip()
                    cnt_num = url.split('idx=')[1].split('&')[0].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'geochimtoren',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': '',
                        'Cnt_writer' : '',
                        'Cnt_vol' : '',
                        'Cnt_fname' : '',
                        'Cnt_chk': 0
                    }
                    print(data)
                    print('=============================================')

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("geochimtoren 크롤링 시작")
    site = ['drama','ent','animation']
    for s in site:
        startCrawling(s)
    print("geochimtoren 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
