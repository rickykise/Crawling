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
    'Host': 'torrentsoda2.site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'https://torrentsoda2.site/'+site+'&mode=list&order_by=fn_pid&order_type=desc&list_type=list&board_page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        try:
            if site.find('영화/국내영화') != -1 or site.find('국내방송/드라마') != -1:
                div = soup.find_all('div', 'post-subject')
                for item in div:
                    title = item.find('a')['title']
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = 'https://torrentsoda2.site'+item.find('a')['href']
                    url = urllib.parse.unquote(url)
                    cnt_num = url.split('vid=')[1].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'torrentsoda2',
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
            else:
                tr = soup.find_all('tr', id=re.compile("mb_+"))
                for item in tr:
                    title = item.find('td', 'text-left').find('a')['title']
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = item.find('td', 'text-left').find('a')['href']
                    url = urllib.parse.unquote(url)
                    cnt_num = url.split('vid=')[1].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'torrentsoda2',
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

    print("torrentsoda2 크롤링 시작")
    site = ['영화/국내영화?board_name=kor_movie', '국내방송/드라마?board_name=drama', '국내방송/예능?board_name=enter', '애니메이션?board_name=animation']
    site = ['영화/국내영화?board_name=kor_movie', '국내방송/드라마?board_name=drama']
    for s in site:
        startCrawling(s)
    print("torrentsoda2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
