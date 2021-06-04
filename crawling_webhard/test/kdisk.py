import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'Intro_domain_chk=kdisk.co.kr; keep_query_string=%2Findex.php%3Fmode%3Dkdisk%26section%3DMOV; _co_t=1552632735; PCID=15526327521206982444012; _ga=GA1.3.1707869253.1552632753; _gid=GA1.3.336618281.1552632753; loadFirst_list=ok; list_type=mnShare_text_list',
    'Host': 'www.kdisk.co.kr',
    'Referer': 'http://www.kdisk.co.kr/index.php?mode=kdisk&section=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest'
}

def startCrawling(site):
    # conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    # curs = conn.cursor(pymysql.cursors.DictCursor)
    with requests.Session() as s:
        i = 0;check = True
        while check:
            i = i+1
            if i == 2:
                break
            link = 'http://www.kdisk.co.kr/main/module/bbs_list_sphinx_proc.php?mode=kdisk&list_row=3&list_count=&p=3&search_type=MOV&search_type2=title&search_keyword=title&sub_sec=&search=&section=MOV&hide_adult=N&blind_rights=N&sort_type=default&sm_search=&sm_search_keyword=&plans_idx=&list_type=mnShare_text_list'
            post_one  = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            print(soup)


if __name__=='__main__':
    start_time = time.time()

    print("bondisk 크롤링 시작")
    site = ['','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("bondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
