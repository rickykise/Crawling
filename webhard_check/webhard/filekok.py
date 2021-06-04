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

cnt_osp = 'filekok'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            token = ''
            with requests.Session() as s:
                Page = {
                    'act': 'get_token'
                }
                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Origin': 'http://www.filekok.com',
                    'X-Requested-With': 'XMLHttpRequest',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                login_token = s.post('http://www.filekok.com/ajax_controller.php', data=Page, headers=headers)
                soup = bs(login_token.text, 'html.parser')
                text = str(soup)
                token = text.split('{"result":"')[1].split('","')[0]

                LOGIN_INFO = {
                        'browser': 'pc',
                        'isSSL': 'Y',
                        'mb_id': 'up0001',
                        'mb_pw': 'up0001',
                        'repage': 'reload',
                        'token': token,
                        'url': '/main/module/loginClass.php',
                        'url_ssl': 'https://ssl.filekok.com/loginClass.php'
                }
                login_req = s.post('https://ssl.filekok.com/loginClass.php', data=LOGIN_INFO, headers=headers)
                post_one  = s.post(url, headers=headers)
                soup = bs(post_one.text, 'html.parser')
                cnt_chk = 0

                if soup.find_all('td', 'txt')[4].find('img'):
                    jehu = soup.find_all('td', 'txt')[4].find('img')['alt']
                    if jehu == '제휴컨텐츠':
                        cnt_chk= 1
                if soup.find('span', 'half_arrow'):
                    jehu = str(soup)
                    if jehu.find('alt="제휴컨텐츠"') != -1:
                        cnt_chk= 1

        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("filekok check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filekok check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
