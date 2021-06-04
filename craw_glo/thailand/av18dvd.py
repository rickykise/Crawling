import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': '__cfduid=d401b7a95e922eec5e75512d15deaeb8b1580189427; ci_session=9d7be45403e268e484d514c6bb0763c2b32e9ec2; _ga=GA1.2.1021508450.1580188257; _gid=GA1.2.1276791688.1580188257; _gat=1; _gat_gtag_UA_139889299_1=1; __atuvc=2%7C5; __atuvs=5e2fc260bb72fae6001',
    'Host': 'av18dvd.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = 'https://av18dvd.com/genre/serieskorea/'
    link2 = '.html'
    while check:
        if i == 192:
            break
        r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'movie-container').find_all('div', 'col-md-2')
        i = i+24

        try:
            for item in div:
                imgUrl = item.find('img')['data-src']
                url = item.find('div', 'movie-title').find('a')['href']
                titleSub = item.find('img')['alt']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'season').find_all('a')

                for item in sub:
                    host_url = item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'av18dvd',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("av18dvd 크롤링 시작")
    startCrawling()
    print("av18dvd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
