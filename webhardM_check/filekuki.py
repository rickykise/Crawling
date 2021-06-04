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

cnt_osp = 'filekuki'

cookies = {'Cookie': 'filekukicookie=200907221b0a72d26c6f0003; _ga=GA1.2.1089495264.1545626114; _gid=GA1.2.1723203492.1545626114; _gat=1; JSESSIONID=59D86CB75C3DAB9DA3A6118B4ECADB50; wcs_bt=a05cd422482044:1545634157'}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                cnt_num = url.split('id=')[1]
                url2 = 'http://www.filekuki.com/popup/kukicontview.jsp?id=' + cnt_num

                post_one  = s.get(url2, cookies=cookies)
                soup = bs(post_one.text, 'html.parser')

                if soup.find('th', scope='col'):
                    cnt_chk = 0
                    if soup.find('p', 'ico_coop'):
                        if soup.find('p', 'ico_coop').find('img', alt='제휴'):
                            cnt_chk = 1
                else:
                    cnt_chk = 2
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filekuki check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filekuki check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
