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

cnt_osp = 'smartfile'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            LOGIN_INFO = {
                'Frame_login': 'Ok',
                'keep': 'Y',
                'm_id': 'enjoy11@naver.com',
                'm_pwd': 'enjoy11'
            }
            headers = {'Cookie': '_ga=GA1.3.1815700316.1545894808; PHPSESSID=ajgp9p5oobd0m23e6do6v9fq67; _gid=GA1.3.1732146722.1548318471; 7b0596d2e793be34d2366c836163650f=MA%3D%3D; 046dd99d5c62a46485c88ba0022a8fa7=dXAwMDAxQG5hdmVyLmNvbQ%3D%3D; Nnum=1; d994c3d58197ed689769fa93d904018a=MTU0ODQwNDkxNw%3D%3D; mecross_box_3333=17818634; storm_sale=F; wcs_bt=79d0ffc89b3d5:1548318599; _gat=1'}
            with requests.Session() as s:
                login_req = s.post('http://smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO, headers=headers)
                r = s.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find('table', summary='컨텐츠정보표').find('tbody')
                cnt_chk = 0

                if table.find_all('td')[2].find('img'):
                    jehu = table.find_all('td')[2].find('img')['title']
                    if jehu == '제휴':
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("smartfile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("smartfile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
