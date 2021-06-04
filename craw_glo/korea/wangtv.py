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

def startCrawling(site):
    i = 0;check = True
    link = 'http://wangtv.co.kr/bbs/board.php?bo_table=wangtv&sca=TV'+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('form', id='fboardlist').find('tbody').find_all('tr')

        try:
            for item in tr:
                cnt_num = item.find('a')['href'].split('wr_id=')[1].split('&')[0]
                url = 'http://wangtv.co.kr/bbs/board.php?bo_table=wangtv&wr_id='+cnt_num
                title = item.find('a').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', id='bo_v_con').find_all('a')

                for item in sub:
                    url2 = item['href']
                    r = requests.get(url2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    host_url = soup.find('a')['href'].replace('..', 'http://wangtv.co.kr')

                    if host_url.find('view/ppvod') != -1:
                        origin_url = host_url
                        origin_osp = 'ppvod'
                    else:
                        origin_url = ''
                        origin_osp = ''

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'wangtv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
                        'cnt_writer': '',
                        'origin_url': origin_url,
                        'origin_osp': origin_osp
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("wangtv 크롤링 시작")
    site = ['드라마', '예능']
    for s in site:
        startCrawling(s)
    print("wangtv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
