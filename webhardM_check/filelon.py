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

cnt_osp = 'filelon'

pcHeaders = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://www.filelon.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                Data = {
                    'act': 'get_token'
                }
                token_req = s.post('http://www.filelon.com/ajax_controller.php', data=Data, headers=pcHeaders)
                soup = bs(token_req.text, 'html.parser')
                token = str(soup).split('"result":"')[1].split('","')[0]

                LOGIN_INFO = {
                    'browser': 'pc',
                    'isSSL': 'Y',
                    'mb_id': 'up0001',
                    'mb_pw': 'up0001',
                    'repage': 'reload',
                    'token': token,
                    'url': '/main/module/loginClass.php',
                    'url_ssl': 'https://ssl.filelon.com/loginClass.php'
                }
                login_req = s.post('https://ssl.filelon.com/loginClass.php', data=LOGIN_INFO, headers=pcHeaders)

                cnt_num = url.split('idx=')[1]
                url2 = 'http://www.filelon.com/main/popup.php?doc=bbsInfo&idx='+cnt_num

                post_two  = s.get(url2, headers=pcHeaders)
                soup2 = bs(post_two.text, 'html.parser')
                table = soup2.find_all('table', 'pop_base')[1]
                cnt_chk = 0

                if table.find('td', 'txt').find('span', 'ic_alliance'):
                    jehu = table.find('td', 'txt').find('span', 'ic_alliance').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_filelon check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_filelon check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
