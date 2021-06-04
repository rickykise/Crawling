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

cnt_osp = 'filemong'

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            cnt_num = url.split('idx=')[1].strip()
            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'crossCookie=bar; PHPSESSID=ogiikktergbpef071apso79hv2',
                'Host': 'filemong.com',
                'Referer': 'https://filemong.com/contents/list.html?section=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest'
            }

            Data2 = {
                'bbs_idx': cnt_num
            }

            with requests.Session() as s:
                link2 = 'https://filemong.com/contents/info_ajax.php'
                post_two  = s.post(link2, headers=headers, data=Data2, allow_redirects=False)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                cnt_price = soup.find('div', 'view-info').find_all('tr')[1].find_all('td')[3].text.split("p")[0].replace(',', '').strip()
                title = soup.find('h2', 'title').text.strip()
                title_null = titleNull(title)

                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                checkPrice = str(keyCheck['p'])
                if checkPrice == cnt_price:
                    cnt_chk = 1

                # print(title)
                # print('판매가 :', cnt_price)
                # print('판매가 :', cnt_price)
                # print(cnt_chk)
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("filemong check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("filemong check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
