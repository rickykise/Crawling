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

def startCrawling():
    i = 0;check = True
    link = 'https://thoctv.com/quoc-gia/han-quoc/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find('div', 'items').find_all('article', 'item movies')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a').find('img')['alt']
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                url = 'https://thoctv.com/xem-phim/running-man-cuoc-dua-bat-dau-21974'
                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                titleEng = soup.find('span', 'tagline').text.strip()
                if titleEng.find('(') != -1:
                    titleEng = titleEng.split('(')[0].strip()
                url2 = soup.find('a', 'nutplay')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                # host_cnt = 1
                li = soup.find('div', 'serverlist').find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    title = titleEng+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'thoctv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
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

    print("thoctv 크롤링 시작")
    startCrawling()
    print("thoctv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
