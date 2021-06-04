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
    link = 'https://kinohd777.ru/board/'+site+'-'

    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', id='allEntries').find_all('div', id=re.compile("entryID+"))

        try:
            for item in div:
                url = 'https://kinohd777.ru'+item.find('div', 'eTitle').find('a')['href']
                title = item.find('div', 'eTitle').find('a').text.strip()
                if title.find('(20') != -1:
                    title = title.split('(20')[0].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                # host_cnt = 1

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'kinohd777',
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

    print("kinohd777 크롤링 시작")
    site = ['zarubezhnye_serialy/19', 'dramy/10']
    for s in site:
        startCrawling(s)
    print("kinohd777 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")