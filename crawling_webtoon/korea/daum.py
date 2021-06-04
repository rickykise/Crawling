import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    link = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/'
    val = ['mon','tue','wed','thu','fri','sat','sun']
    for v in val:
        try:
            r = requests.get(link+v)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            json_obj = json.loads(text)

            for item in json_obj['data']:
                ageGrade = item['ageGrade']
                if ageGrade >= 19:
                    continue
                nickName = item['nickname']
                url = 'http://webtoon.daum.net/webtoon/view/'+nickName
                title = item['title']
                title_check = titleNull(title)

                i = 0;check = True
                host_url = 'http://webtoon.daum.net/data/pc/webtoon/view/'+nickName
                r = requests.get(host_url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text2 = str(soup)
                json_obj2 = json.loads(text2)
                data = json_obj2['data']
                webtoon = data['webtoon']
                webtoonEpisodes = webtoon['webtoonEpisodes']

                for item in webtoonEpisodes:
                    craw_url = 'http://webtoon.daum.net/webtoon/viewer/'+str(item['id'])
                    title_num = item['title'].split('화')[0].strip()

                    data = {
                        'craw_osp_id': 'daum',
                        'craw_domain': 'net',
                        'craw_title': title,
                        'craw_site_url' : url,
                        'craw_url': craw_url,
                        'craw_title_num': title_num
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("daum 크롤링 시작")
    startCrawling()
    print("daum 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
