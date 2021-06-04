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

cnt_osp = 'netfile'

LOGIN_INFO = {
    'action_event': 'memberLogin',
    'enid': 'dXAwMDAz',
    'id': 'up0003',
    'passwd': 'up0003',
    'pwd': 'dXAwMDAz',
    'url': '/index_front.jsp'
}

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'pop_170926=check; wcs_bt=3bc7e16471d78:1553837240; JSESSIONID=3579B3EE15AFF7AE9C816992ABBA95BC; referer_url=direct; __utmz=210917130.1553745088.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=210917130.662225564.1553745088.1553757728.1553834516.4; __utmb=210917130.47.10.1553834516; __utmc=210917130; __utmt=1',
    'Host': 'www.netfile.co.kr',
    'Referer': 'https://www.netfile.co.kr/index_front.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                login_req = s.post('http://www.netfile.co.kr/member-action.do', headers=headers, data=LOGIN_INFO)
                post_two  = s.get(url)
                soup = bs(post_two.text, 'html.parser')
                cnt_chk = 0

                title = soup.find('p', 'mediaView_name').text.strip()
                title_null = titleNull(title)
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                checkPrice = str(keyCheck['p'])
                cnt_price = soup.find('span', 'coin').text.split("코인")[0].replace(',', '').strip()
                if checkPrice == cnt_price:
                    cnt_chk = 1

        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("applefile check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("applefile check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
