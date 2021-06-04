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

# headers = {
#     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'ko-KR',
#     'Connection': 'Keep-Alive',
#     'Host': 'gall.dcinside.com',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
# }

# def checkbili(title):
#     check = True
#     if title.find('2017') != -1 or title.find('2018') != -1 or title.find('2019') != -1 or title.find('2020') != -1 or title.find('2021') != -1:
#         check = False
#
#     s = 1700
#     for i in range(12):
#         s = s+1
#         if title.find(str(s)) != -1:
#             check = False
#
#     e = 1800
#     for i in range(12):
#         e = e+1
#         if title.find(str(e)) != -1:
#             check = False
#
#     n = 1900
#     for i in range(12):
#         n = n+1
#         if title.find(str(n)) != -1:
#             check = False
#
#     t = 2000
#     for i in range(12):
#         t = t+1
#         if title.find(str(t)) != -1:
#             check = False
#
#     a = 2100
#     for i in range(12):
#         a = a+1
#         if title.find(str(a)) != -1:
#             check = False
#
#     return check

def startCrawling():
    # http://dint.img18.kr/dint_board/tvspon/20171012/20171012_6_2.jpg
    # http://dint.img18.kr/dint_board/tvspon/20170801_1_1.jpg
    # http://dint.img18.kr/dint_board/20181122_4_2.jpg

    # link = 'http://dint.img18.kr/dint_board/20181122_4_2.jpg'
    # print(link)
    # if link.find('tvspon/') != -1:
    #     d_thum = link.split('tvspon/')[1].strip()
    #     if d_thum.count('/') == 1:
    #         d_thumbnail = d_thum.split('/')[1].split('.')[0].strip()
    #     else:
    #         d_thumbnail = d_thum.split('.')[0].strip()
    # else:
    #     d_thum = link.split('board/')[1].strip()
    #     d_thumbnail = d_thum.split('.')[0].strip()
    # print(d_thumbnail)

        # if d_thum.count('/')
    # r = requests.get('https://doramy.net/1839-legenda-sinego-morya-yuzhnaya-koreya-2016.html')
    # c = r.content
    # soup = BeautifulSoup(c,"html.parser")
    #
    # print(soup)

    # <script type="text/javascript">location.replace("/derror/deleted/giants_new");</script>

    # getIMG = getImage()
    # print(getIMG)

    # url = 'dramacool.video'
    # dot = url.count('.')
    # print(dot)

    # a = 1700
    # for i in range(12):
    #     a = a+1
    #     print(a)
    #
    # print(a)
    # title_null = '2010tv'
    # chekb = checkbili(title_null)
    # if chekb == False:
    #     print('패스')


    # testNum = 0
    # now = datetime.datetime.now().strftime('%Y-%m-%d')
    # print(type(now))
    # url = 'https://video.tudou.com/v/XNDQyMDE2NDY0NA==.html?from=s1.8-1-1.2'
    # testNum = testNumget('2019-10-01', url)
    # if testNum >= 1:
    #     print('실패')
    #     sys.exit(1)
    # print('성공')

    title = 'Không Ai Hay Biết'
    title_null = titleNull(title)
    print(title_null)

    # 키워드 체크
    getKey = getKeyword()
    keyCheck = checkTitle(title_null, getKey)
    print(keyCheck['m'])

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
