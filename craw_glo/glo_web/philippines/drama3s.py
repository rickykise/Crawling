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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)


def startCrawling():
    i = 0;check = True
    link = 'https://wvw.drama3s.to/country/korean-i1-'
    link2 = '.html'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cookie': '_ga=GA1.2.2007388592.1567991981; __cfduid=df85b15d81d1132bd6cdd8a929f3cf45e1567991975; cf_clearance=cd373cdfd506fb3d8b57c1ac57206d7de0a6d0ba-1568099216-1800-150',
                'Host': 'wvw.drama3s.to',
                'Referer': link+str(i)+link2,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }

            r = requests.get(link+str(i)+link2, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            li = soup.find('ul', 'list-film').find_all('li')

            try:
                for item in li:
                    url = 'https://wvw.drama3s.to'+item.find('a')['href']
                    titleSub = item.find('a')['title']
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
                    url2 = 'https://wvw.drama3s.to'+soup.find('a', 'btn-see btn btn-danger')['href']

                    r = requests.get(url2, headers=headers)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('ul', 'list-episode')

                    for item in div:
                        li = item.find_all('li')
                        for item in li:
                            host_url = 'https://wvw.drama3s.to'+item.find('a')['href']
                            title = titleSub + '_' + item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'drama3s',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'philippines',
                                'cnt_writer': '',
                                'origin_url': '',
                                'origin_osp': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("drama3s 크롤링 시작")
    startCrawling()
    print("drama3s 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
