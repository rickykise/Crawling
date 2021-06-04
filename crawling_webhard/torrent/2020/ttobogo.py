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
    link = 'https://ttobogo.net/search?skeyword='+key+'&page='
    while check:
        i = i+1
        if i == 10:
            break
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cookie': 'HstCnv4351400=2; HstCmu4351400=1579154616308; __dtsu=1EE70445BDFCC95D3A308B04026B78D7; HstCfa4351400=1579154616308; HstPt4351400=3; HstPn4351400=1; HstCla4351400=1579225145207; HstCns4351400=2; __cfduid=d61453a0ac9e13447ce6b3d2696379f051579154623; cf_clearance=573a2c972151883ab841703e4b0c3bf1873b91b6-1579225142-0-150; csrf_cookie_name=86fb19c7388e03e9a8b2d592aace1a63; ci_session=hl6p3cq1o9rbbrhv0ken8vn9opqtg3mj',
            'Host': 'ttobogo.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        count = soup.find('ul', 'list-body').find_all('li')
        if len(count) <= 1:
            break
        li = soup.find('ul', 'list-body').find_all('li', 'list-item')

        try:
            for item in li:
                title = item.find('a', 'subject').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                keyCheck = checkTitle(title_null, keywordCh)
                if keyCheck == None:
                    continue

                url = item.find('a', 'subject')['href']
                cnt_num = url.split('post/')[1]

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'ttobogo',
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

    print("ttobogo 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("ttobogo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
