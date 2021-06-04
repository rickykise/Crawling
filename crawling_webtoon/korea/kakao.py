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
    link = 'https://api2-page.kakao.com/api/v8/store/section_container/list?agent=web&category=10&subcategory=1000&day=0'
    r = requests.get(link)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)
    json_obj = json.loads(text)

    for i in json_obj['section_containers']:
        list = i['section_series']
        try:
            for i in list:
                get_list = i['list']
                for item in get_list:
                    if item['age_grade'] >= 15:
                        continue
                    series_id = str(item['series_id'])
                    url = 'https://page.kakao.com/home?seriesId=' + series_id
                    title = item['title']
                    title_check = titleNull(title)

                    i = 0;check = True
                    host_url = 'https://api2-page.kakao.com/api/v5/store/singles'
                    while check:
                        # try:
                        if i == 30:
                            break
                        Data = {
                            'direction': 'desc',
                            'page': i,
                            'page_size': '20',
                            'seriesid': series_id,
                            'without_hidden': 'true'
                        }
                        i = i+1

                        r = requests.post(host_url, data=Data)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        text = str(soup)
                        json_obj2 = json.loads(text)
                        if json_obj2['singles'] == []:
                            i = 0
                            break

                        for item in json_obj2['singles']:
                            craw_url = 'https://page.kakao.com/viewer?productId='+str(item['id'])
                            title_num = item['title'].split('화')[0].strip()
                            check_num = title_num.replace(' ', '')
                            if check_num.find(title_check) != -1:
                                title_num = check_num.split(title_check)[1].strip()

                            data = {
                                'craw_osp_id': 'kakao',
                                'craw_domain': 'com',
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

    print("kakao 크롤링 시작")
    startCrawling()
    print("kakao 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
