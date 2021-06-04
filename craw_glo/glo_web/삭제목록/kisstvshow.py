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

def startCrawling():
    i = 0;check = True
    link = 'http://kisstvshow.to/Country/South-Korea?page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            link = link+str(i)
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep',
                'Cookie': '__test; __cfduid=da32d608f57f3bfd4ca749bc81408b8c01561703231; _ga=GA1.2.1504971441.1561703233; _gid=GA1.2.1952603345.1561703233; __PPU_SESSION_1_2454905_false=1561703255589|1|1561703255589|1|1',
                'Host': 'kisstvshow.to',
                'Referer': link,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            post_one = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', 'list-show').find_all('div')

            try:
                for item in div:
                    url = 'http://kisstvshow.to'+item.find('a')['href']
                    titleSub = item.find('span', 'title')
                    title_check = titleNull(titleSub)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue

                    post_two = s.get(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    tr = soup.find('table', 'listing').find_all('tr')

                    for item in tr:
                        td = item.find_all('td')
                        if len(td) != 0:
                            cnt_url = 'http://kisstvshow.to'+item.find('a')['href']
                            cnt_num = cnt_url.split('id=')[1]
                            title = item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_num' : cnt_num,
                                'cnt_osp' : 'kisstvshow',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'cnt_url' : cnt_url,
                                'cnt_host' : '',
                                'cnt_writer' : '',
                                'cnt_nat': 'philippines'
                            }
                            # print(data)

                            dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("kisstvshow 크롤링 시작")
    startCrawling()
    print("kisstvshow 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
