import requests,re
import sys
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
    'Cookie': 'Intro_domain_chk=kdisk.co.kr; keep_query_string=%2Findex.php%3Fmode%3Dkdisk%26section%3DMOV; _co_t=1552632735; PCID=15526327521206982444012; _ga=GA1.3.1707869253.1552632753; _gid=GA1.3.336618281.1552632753; _gat_UA-57089340-2=1; bvent=0; mid=0a191a191a191a19h619c619; UID=up0001; nick=up0001; mp_info2=1; Lidx=%241%24JAA7Nsf8%24BzJ9zwsDWx8nkXCZUmwxv.; noinChk=kmain; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; SetT=%0D%85H%F9%7C%84%15%D0%D9%82%DB%86hYu%AE%95%E7%98%1FxP%97%FD%8A%E7%A6; SCkey=MGExOTFhMTkxYTE5MWExOWg2MTljNjE5fHVwMDAwMXw%253D; charge=no; loadFirst_list=ok; list_type=mnShare_text_list',
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
            link = 'http://kdisk.co.kr/main/module/bbs_list_sphinx_proc.php?mode=kdisk&list_row=1&list_count=&p=1&search_type=MOV&search_type2=title&search_keyword=title&sub_sec=&search=&section=MOV&hide_adult=N&blind_rights=N&sort_type=comment_rank&sm_search=&sm_search_keyword=&plans_idx=&list_type=mnShare_text_list'
            sys.setrecursionlimit (2000)
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            print(soup)


if __name__=='__main__':
    start_time = time.time()

    print("kdisk 크롤링 시작")
    # site = ['','MOV','DRA','MED','ANI']
    site = ['']
    for s in site:
        startCrawling(s)
    print("kdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
