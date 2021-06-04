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
    i = 0;check = True;result = [];check_url = ''
    link = 'http://onairseries-subthai.com/type/korea?page='
    while check:
        i = i+1
        if i == 40:
            break
        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Cookie': '__cfduid=d00fa965a70db9cc2f36dec46320d5a731620002543; XSRF-TOKEN=eyJpdiI6InJtZWdjbnJTR3o3QTRZd2FaNjJJanc9PSIsInZhbHVlIjoiTlIxbzlETXRPUW8xNUZzdjFVVVJSaWRvNEcxcW5zdnBkdkd3Znk1MEpWeDVEZlM2U2pZWWVqS2Rxa05oVDV2MyIsIm1hYyI6IjkyMjQ4NWEzYThmNTQwODFmNzI2ODJjOWU3YjQ3NGFiZjNmOGYxOWYyYjIzMDllOWRkODRjNzUyYjY2YTEzNzAifQ%3D%3D; laravel_session=eyJpdiI6Ikp1SUlvaGhWMWxlc2p4RlwvOTJXWWJ3PT0iLCJ2YWx1ZSI6IlFBbFJKMW9XUVl6WCtpNHc1akdhbkNSamNKMTZlWmhIMTIwTlZlN0RoZnNpNXpFXC9BYVdPZWJIeXpsbDYrTjc1IiwibWFjIjoiMDNhZWNkMDc2ZDJiZTBhZjQ4ZjQ5NTg1ZWVkZWFiZTI2YmI5YTEzZjI5NjIyMzA2MzJkNjMzMjdkMTIxNDIxNyJ9; _ga=GA1.2.866249275.1620002545; _gid=GA1.2.1007324840.1620002545; _gat_gtag_UA_149712383_1=1',
            'Host': 'onairseries-subthai.com',
            'Referer': 'http://onairseries-subthai.com/type/korea',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest'
        }

        data = {
            'page': str(i)
        }

        r = requests.get(link+str(i), headers=headers, data=data)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'col-lg-9').find_all('a', 'col-md-12')

        try:
            for item in div:
                url = 'http://onairseries-subthai.com'+item['href']
                titleSub = item.find('h3', 'text-white').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                for u in result:
                    if u == url:
                        check_url = url

                if check_url != '':
                    check_url = ''
                    continue
                result.append(url)

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('div', 'row mt-lg-4').find_all('a')

                for item in sub:
                    host_url = 'http://onairseries-subthai.com'+item['href']
                    title = titleSub+'_'+item.find('div', 'text-left').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'onairseries-subthai',
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
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("onairseries-subthai 크롤링 시작")
    startCrawling()
    print("onairseries-subthai 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
