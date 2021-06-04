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

cnt_osp = 'daoki'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            r = requests.get('http://oradisk.com/')
            c = r.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            captcha_aes = soup.find('input', id='captcha_aes')['value']
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'captcha_aes': captcha_aes,
                'fromsite': 'oradisk',
                'idSave': '0',
                'm': '',
                'm_id': 'up0001',
                'm_pwd': 'up0001'
            }
            with requests.Session() as s:
                login_req = s.post('http://daoki.com/member/loginCheck.php', data=LOGIN_INFO)
                cnt_num = url.split('idx=')[1].split('&')[0]
                aes = url.split('aes=')[1]
                url2 = 'http://daoki.com/contents/view_top_filedown_new.html?idx='+cnt_num+'&aes='+aes

                post_two  = s.get(url2)
                c = post_two.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                cnt_chk = 0
                jehu = soup.find_all('table')[5].find_all('td')[2].find('img')['src']
                if jehu.find('allri_icon') != -1:
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("daoki check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("daoki check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
