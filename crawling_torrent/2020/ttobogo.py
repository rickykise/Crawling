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
            'Cookie': '__cfduid=dfd29602886a5d188e641c8f14fba3a3e1579154614; cf_clearance=4f8b8ccb3abe88ae761ceab7af61a328c23e9362-1579154614-0-150; csrf_cookie_name=aa6fd420f52a70710f7f434a3d081fc5; ci_session=fvkam30h5arib5h74g8tkrmh05m162ua; HstCfa4351400=1579154616308; HstCla4351400=1579154616308; HstCmu4351400=1579154616308; HstPn4351400=1; HstPt4351400=1; HstCnv4351400=1; HstCns4351400=1; __dtsu=1EE70445BDFCC95D3A308B04026B78D7',
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
