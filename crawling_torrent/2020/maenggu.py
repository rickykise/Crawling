import requests,re
import pymysql,time,datetime
import urllib.parse
from webhardFun import *
from urllib.parse import unquote
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'maenggu.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key):
    keyword = key
    keywordCh = keyword.replace(' ', '')
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://maenggu.com/search.php?q='+key

    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        if soup.find('ul', 'list'):
            li = soup.find('ul', 'list').find_all('li')

            try:
                for item in li:
                    title = item.find('div', 'title').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    keyCheck = checkTitle(title_null, keywordCh)
                    if keyCheck == None:
                        continue

                    url = 'https://maenggu.com/'+item.find('a')['href']
                    cnt_num = url.split('idx=')[1]

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'maenggu',
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
        else:
            break

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeyword()

    print("maenggu 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("maenggu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
