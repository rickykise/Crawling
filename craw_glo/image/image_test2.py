import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.90s.tw/index.php?s=home-vod-type-id-'+site
    link2 = '-mcid--area--year--letter--order--picm-1-p-'
    if site == '4':
        link2 = '-mcid--area-%E9%9F%A9%E5%9B%BD-year--letter--order--picm-1-p-'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+link2+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'box-video-list').find_all('li')

        # try:
        for item in li:
            imgUrl = item.find('a')['data-original']
            # imgUrl = 'https://www.emons.co.kr/upload_files/board/drama/1558913990_9795_1.jpg'
            # imgUrl = 'http://61.82.113.196:8181/poster/poster.jpg'
            otoImg = 'http://pic.szjal.cn/img/5d82d7af10e3d.jpg'
            url = 'https://www.90s.tw'+item.find('div', 'title').find('a')['href']

            titleSub = item.find('div', 'title').find('a').text.strip()
            title_check = titleNull(titleSub)
            # 키워드 체크
            # getKey = getKeyword()
            # keyCheck = checkTitle(title_check, getKey)
            # if keyCheck['m'] == None:
            #     continue
            # cnt_id = keyCheck['i']
            # cnt_keyword = keyCheck['k']

            # 2개의 이미지 비교
            img_check = imgCheck(otoImg, imgUrl)
            print(imgUrl)
            print(titleSub)
            print(img_check)
            print("=================================")

            # r = requests.get(url)
            # c = r.content
            # soup = BeautifulSoup(c,"html.parser")
            # li = soup.find('div', 'playlist').find_all('li')

            # for item in li:
            #     host_url = 'https://www.90s.tw'+item.find('a')['href']
            #     title = titleSub+'_'+item.find('a').text.strip()
            #     title_null = titleNull(title)
                # host_cnt = 1

                # data = {
                #     'cnt_id': cnt_id,
                #     'cnt_osp' : '90s',
                #     'cnt_title': title,
                #     'cnt_title_null': title_null,
                #     'host_url' : host_url,
                #     'host_cnt': '1',
                #     'site_url': url,
                #     'cnt_cp_id': 'sbscp',
                #     'cnt_keyword': cnt_keyword,
                #     'cnt_nat': 'indonesia',
                #     'cnt_writer': '',``
                #     'cnt_cate': img_check,
                #     'origin_url': '',
                #     'origin_osp': ''
                # }
                # print(data)
                # print("=================================")

                    # dbResult = insertALL(data)
        # except:
        #     continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("90s 크롤링 시작")
    site = ['23', '4']
    for s in site:
        startCrawling(s)
    print("90s 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
