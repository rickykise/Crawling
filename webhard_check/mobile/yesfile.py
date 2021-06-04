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

cnt_osp = 'yesfile'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                post_two  = s.get(url)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                cnt_chk = 0

                if soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].find('span'):
                    cnt_chk = 1
                if cnt_chk == 0:
                    if soup.find('div', 'fileinfo_imgarea'):
                        jehu = soup.find('div', 'fileinfo_imgarea')
                        textjehu = str(jehu)
                        if textjehu.find('icn_list_100.png') != -1:
                            cnt_chk = 1
                if soup.find('div', 'c_size'):
                    jehuent = soup.find('div', 'c_size').find('img')['src']
                    if jehuent.find('kbsent') != -1:
                        cnt_chk = 1
                    else:
                        jehuent = soup.find_all('div', 'c_size')[1].find('img')['src']
                        if jehuent.find('kbsent') != -1:
                            cnt_chk = 1
                    if soup.find('div', 'c_size').find('img'):
                        jehuent = soup.find('div', 'c_size').find('img')['src']
                        if jehuent.find('icn_list_sale') != -1:
                            cnt_price = soup.find('div', 'fileinfo_textarea').find_all('li', 'info_a')[1].find('strong').text.split('P')[0].replace(",","").strip()
                            cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_yesfile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_yesfile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")