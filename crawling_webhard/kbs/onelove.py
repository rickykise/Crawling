import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling():
    i = 0;a = 1;check = True
    link = "https://pbbsapi.kbs.co.kr/board/v1/list?bbs_id=T2019-0029-01-904250&page=1&page_size=10&notice_yn=Y&kbs_board_auth=0"
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        # print(soup)
        text = str(soup)
        try:
            for item in text:
                cnt_num = text.split('{"id":')[a].split(',"bbs_id"')[0]
                print(cnt_num)

                a = a+1
        except:
            continue



if __name__=='__main__':
    start_time = time.time()

    print("onelove 크롤링 시작")
    startCrawling()
    print("onelove 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
