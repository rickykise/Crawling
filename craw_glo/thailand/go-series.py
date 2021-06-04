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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__cfduid=d2d3accee2513bcf1ec9e9f6fb452377d1610949739',
    'Host': 'go-series.com',
    'Referer': 'https://go-series.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = 'https://go-series.com/?__cf_chl_jschl_tk__=1dca6b3020bebf88fe672bda5a2933e147cb3f1c-1610949739-0-AYLoXlvc1eYL8G_7Jrz2lV3fhqGXJUd2VH4BFP2_sL9FAEv30EmDxednkgf3ET6hQxIXtHCUSwuBfuj9C1NYREBTz9T6vZ8zxkjAhcxz6Zcdq9gwIMNmVPjKliQ37DFpbGwV94teZe4wxygzZxRK3vxPSjbjUxTN6GEA29lQnlO4vUPSb0mAe0OMJrb8DMsVXkBGyTiQK_l2VOeRv6HyQgfAAxs5N9QgknVQnXrz9_q7hInwpu86AaPPGwfgywQqfJwOVaC0EQynZDMfPPeum0lAv0N7dZ0yO-62ki8wb_7hWks6kzt-cls5UrfS9kQqDi6j86ggV_ezuMbDB66B9OFFjmeDiHIPEWMkmWmnl7rw6xsD6fUZBbgoeQdvyIEJ2A'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.post(link, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")

        link2 = 'https://go-series.com/category/2/?p='
        r = requests.post(link2+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'iw_grid')

        try:
            for item in div:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('a')['alt']
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
                sub = soup.find('div', id='content').find_all('a')

                for item in sub:
                    host_url = item['href']
                    host_url = urllib.parse.unquote(host_url)
                    title = item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'go-series',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("go-series 크롤링 시작")
    startCrawling()
    print("go-series 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
