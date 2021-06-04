import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'http://tvonline.starstvs.com/?s='+keyword+'&page='
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 20:
                break
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            if soup.find('figure' ,'gallery'):
                sub = soup.find_all('figure' ,'gallery')

                for item in sub:
                    url = 'http://tvonline.starstvs.com/'+item.find('a')['href']
                    host_url = url
                    title = item.find('a')['title']
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
                        'cnt_osp' : 'starstvs',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': ''
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
            else:
                break
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getKey = getKeywordCH()

    print("starstvs 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("starstvs 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
