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

cnt_osp = 'fileman'

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=cc7prkncvotlnfidibd3cbcfd5; 07099283cfc31f2d473bf5b4628ab3a6=dXAwMDAx',
    'Host': 'fileman.co.kr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'idSave': '0',
                'm_id': 'up0001',
                'm_pwd': 'up0001',
                'x': '37',
                'y': '29'
            }
            with requests.Session() as s:
                login_req = s.post('https://fileman.co.kr/member/loginCheck.php', data=LOGIN_INFO)

                cnt_num = url.split('idx=')[1]
                url2 = 'http://fileman.co.kr/contents/view_top.html?idx='+cnt_num+'&amp;page='
                post_two  = s.get(url2, headers=headers)
                content = post_two.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                text = str(soup)
                cnt_chk = 0

                if soup.find('span', 'main_title'):
                    if text.find('저작권자와의 제휴') != -1:
                        cnt_chk = 1
                else:
                    cnt_chk = 2
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_fileman check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_fileman check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
