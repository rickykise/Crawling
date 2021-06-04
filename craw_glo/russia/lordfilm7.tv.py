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

headers={
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,th;q=0.6,zh-CN;q=0.5,zh;q=0.4',
    'Cache-Control': 'no-cache',
    'Connection':'keep-alive',
    'Cookie': '__cfduid=dccf6d424534673fc5533f08565bc31181594284015; PHPSESSID=02f3fe4e495d12567f67e1119bfe24a4; _ga=GA1.2.1386472812.1594284016; _gid=GA1.2.178551004.1594284016; _ym_uid=1594284016592386853; _ym_d=1594284016; _ym_wasSynced=%7B%22time%22%3A1594284016729%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; _ym_isad=2; _ym_visorc_51186131=b',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}

def startCrawling():
    i = 0;check = True
    link = 'http://v1.lordfilm7.tv/f/country=%D0%9A%D0%BE%D1%80%D0%B5%D1%8F/r-year=1915;2020/r-kp=0;10/r-imdb=0;10/order=desc/page/{}/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', id='dle-content').find_all('a','short-poster')

        try:
            for item in sub:
                url = 'http://v1.lordfilm7.tv'+item['href']
                title = item.find('img')['alt'].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'lordfilm7.tv',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'russia',
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

    print("lordfilm7.tv 크롤링 시작")
    startCrawling()
    print("lordfilm7.tv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
