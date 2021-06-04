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
                post_one  = s.get(url)
                content = post_one.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                text = str(soup)
                tr = soup.find('table', cellspacing='1').find_all('tr')[1]
                cnt_chk = 0

                cnt_price = tr.find_all('td')[6].text.strip().replace("\n","").replace("\t","").replace(" ","").split("P")[0]
                cnt_fname = soup.find('span', 'font_layerlist').text.strip()
                if cnt_fname == "/":
                    cnt_fname = soup.find_all('span', 'font_layerlist')[1].text.strip()
                if text.find('저작권자와의 제휴') != -1:
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("fileman check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("fileman check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
