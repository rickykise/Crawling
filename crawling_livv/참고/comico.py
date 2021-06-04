import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import json
import requests, json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;check = True
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
        'Content-Length': '99',
        'content-type': 'application/json',
        'Host': 'www.comico.kr',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'x-adult-allow': 'false',
        'x-device-id': 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
        'x-device-locale': 'ko',
        'x-device-type': 'DV02',
        'x-time-zone': 'Asia/Seoul'
    }
    link = 'https://www.comico.kr/justoon/api/comic/serial/dayofweek'
    while check:
        i = i+1
        if i == 30:
            break
        print(i)
        data = {
            "pageNo": i,
            "rowsPerPage": "20",
            "criteria": {
                "serialDay": "127",
                "sortType": "0"
            }
        }
        r = requests.post(link, headers=headers, data=json.dumps(data))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        print(text)
        json_obj = json.loads(text)
        print(json_obj)

        try:
            for item in json_obj['rows']:
                contentId = item['contentId']
                url = 'https://www.comico.kr/content/home/' + contentId
                title = item['title']

                a = 0;check = True
                while check:
                    a = a+1
                    if a == 30:
                        break
                    host_url = 'https://www.comico.kr/justoon/api/content/episodes?contentId='+str(contentId)+'&pageNo='+str(a)+'&rowsPerPage=50&order=B&latest='

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text2 = str(soup)
                    json_obj2 = json.loads(text2)
                    grid = json_obj2['grid']
                    rows = grid['rows']
                    if rows == []:
                        break

                    for item in rows:
                        craw_url = url+'/viewer/'+str(item['episodeId'])
                        title_num = item['title'].split('화')[0].strip()

                        data = {
                            'craw_osp_id': 'comico',
                            'craw_domain': 'kr',
                            'craw_title': title,
                            'craw_site_url' : url,
                            'craw_url': craw_url,
                            'craw_title_num': title_num
                        }
                        # print(data)
                        # print("=================================")

                        # dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("comico 크롤링 시작")
    startCrawling()
    print("comico 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
