import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *
from selenium import webdriver

cnt_osp = 'filenori'

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'JSESSIONID=037D42999513B9AFF91DB9E57C331A9B; mEventDesignVer=1060',
    'Host': 'm.filenori.com',
    'Referer': 'http://m.filenori.com/Mobile/home.do',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                post_two  = s.get(url, headers=headers)
                content = post_two.content
                soup = bs(content.decode('utf-8','replace'), 'html.parser')
                text = str(soup)
                cnt_chk = 0

                if soup.find('span', 'pshipIcon'):
                    jehu = soup.find('span', 'pshipIcon').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1
                if text.find('존재하지 않는 컨텐츠') != -1:
                    cnt_chk = 2
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)


if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filenori check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filenori check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
