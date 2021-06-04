import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from checkFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

def startCrawling(url, cnt_id):
    try:
        chk_num = 0; cnt_id = cnt_id[0]
        check_id = getCheckKey()
        keyCheck = checkId(cnt_id, check_id)

        if keyCheck['m'] == None:
            chk_num = '3'
            dbUpResult = googleDelUpdate(chk_num, url)
            pass

        url = urllib.parse.unquote(url)
        link = 'https://www.google.com/search?q='+url
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        time.sleep(3)


        if text.find('일치하는 검색결과가 없습니다') != -1:
            chk_num = '2'
            dbUpResult = googleDelUpdate(chk_num, url)
            # print('삭제됨 : '+chk_num)
        else:
            chk_num = '1'
            dbUpResult = googleDelUpdate(chk_num, url)
            # print('살아있음 : '+chk_num)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getGoogleDel()

    print("google 크롤링 시작")
    for u, c in getKey.items():
        startCrawling(u, c)
    print("google 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
