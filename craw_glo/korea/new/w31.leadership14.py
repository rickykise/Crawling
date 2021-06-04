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
    link = 'https://w31.leadership14.site/bbs/board.php?bo_table='+site+'&page='
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
                if len(item['class']) >= 1:
                    continue
                url = item.find('td', 'fz_subject').find_all('a')[1]['href']
                title = item.find('td', 'fz_subject').find_all('a')[1].text.replace('★', '').strip()
                if title.find('댓글') != -1:
                    title = title.split('댓글')[0].strip()
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
                sub = soup.find('div', style="width:100%;").find_all('a')

                for item in sub:
                    host_url = item['href']

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'w20.leadership14',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
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

    print("leadership14 크롤링 시작")
    site = ['dramakor', 'dramaend', 'enter']
    for s in site:
        startCrawling(s)
    print("leadership14 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
