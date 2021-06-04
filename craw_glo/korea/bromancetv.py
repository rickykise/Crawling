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
    link = 'https://geek.bromancetv.pw/bbs/board.php?bo_table=brotv_'+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list-body').find_all('li', 'list-item')

        try:
            for item in li:
                url = item.find('a')['href']
                if url.find('&page=') != -1:
                    url = url.split('&page=')[0]
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
                sub = soup.find('div', 'view-content').find_all('a')

                for item in sub:
                    host_url = item['href']

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    origin_url = soup.find('iframe')['src']

                    if origin_url.find('https') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bromancetv',
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

    print("bromancetv 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("bromancetv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
