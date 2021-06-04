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

   # Cookie: __cfduid=d2e57e2df44f8b778f8497f65d6061f451605502074; HstCfa4358793=1605502054203; HstCla4358793=1605502054203; HstCmu4358793=1605502054203; HstPn4358793=1; HstPt4358793=1; HstCnv4358793=1; HstCns4358793=1; ppu_main_d950642c2754422085dad9b0d7bf9d9b=1; dom3ic8zudi28v8lr6fgphwffqoz0j6c=2577dd5c-b034-404d-9d32-5922fd7ec665%3A2%3A1; __dtsu=6D00160550205768CE98B89B5C2F4EE6; 494668b4c0ef4d25bda4e75c27de2817=2577dd5c-b034-404d-9d32-5922fd7ec665:2:1

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Host': 'migtidefill.rest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'http://migtidefill.rest/category/'+site+'?country=korean&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(link+str(i))
        print(soup)
        div = soup.find('div', 'item-lists').find_all('div', 'mb40')

        try:
            for item in div:
                url = 'http://migtidefill.rest' + item.find('a')['href']
                titleSub = item.find('h3', 'text-white').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find('div', 'episode-list').find_all('div', 'mb10')

                for item in div:
                    host_url = 'http://migtidefill.rest' + item.find('a')['href']
                    title = item.find('h3').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'migtidefill',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
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

    print("migtidefill 크롤링 시작")
    site = ['drama','k-show']
    for s in site:
        startCrawling(s)
    print("migtidefill 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
