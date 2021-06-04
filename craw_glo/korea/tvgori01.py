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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True; subI = 0; check_Title = ''; firstCheck = True
    link = 'https://tvgori01.com/'+site+'/main?&mca_=1&cpa_='
    link2 = '#a'
    while check:
        checkSub = True
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find('div', 'list').find_all('a', 'boxs')

        try:
            for item in sub:
                url = 'https://tvgori01.com'+item['href']
                if url.find('&mca') != -1:
                    url = url.split('&mca')[0]
                titleSub = item.find('div', 'stit').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', 'link').find_all('div', 'btns')
                title = soup.find('div', 'tcon').find('div', 'titl').text.strip()
                title_null = titleNull(title)

                for item in div:
                    cnt_num = item['onclick'].split("select('")[1].split("',")[0]
                    typ = item['onclick'].split("', '")[1].split("',")[0]
                    num = item['onclick'].split("', '")[2].split("')")[0]
                    host_url = 'https://tvgori.kr/vods?idx_='+cnt_num+'&typ_='+typ+'&num_='+num

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'tvgori01',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'southkorea',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tvgori01 크롤링 시작")
    site = ['drama', 'enter']
    for s in site:
        startCrawling(s)
    print("tvgori01 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
