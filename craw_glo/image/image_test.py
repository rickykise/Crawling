import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from test import *
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            link = 'http://kanbo8.com/'+site+'/index'
            link2 = '.html'
            r = requests.get(link+link2)
        else:
            link = 'http://kanbo8.com/'+site+'/index-'
            link2 = '.html'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'mui-table-view').find_all('li')

        try:
            for item in li:
                imgUrl = 'http://kanbo8.com'+item.find('img')['data-original']
                url = 'http://kanbo8.com'+item.find('a')['href']
                titleSub = item.find('div', 'type-title').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                otoImg = 'http://61.82.113.196:8181/poster/poster.jpg'
                img1 = url_to_image(otoImg)
                img2 = url_to_image(imgUrl)
                # 2개의 이미지 비교
                img_check = diffImg(img1, img2)

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'page3').find_all('ul', class_=False)

                for item in sub:
                    li = item.find_all('a')
                    for item in li:
                        host_url = 'http://kanbo8.com'+item['href']
                        if host_url.find('video') == -1:
                            continue
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'kanbo8',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'indonesia',
                            'cnt_writer': '',
                            'cnt_cate': img_check,
                            'origin_url': '',
                            'origin_osp': ''
                        }
                #         print(data)
                #         print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kanbo8 크롤링 시작")
    site = ['ribenju','zongyi']
    for s in site:
        startCrawling(s)
    print("kanbo8 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
