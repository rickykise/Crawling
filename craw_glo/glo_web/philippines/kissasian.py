import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True;rcheck = True;
    link = 'https://kissasian.sh/Country/South-Korea?page='
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 30:
                break
            cookie = 'cf_clearance=2e8e0d98795d858cc8a8fdec2d5b3c6aff1d51cb-1569371463-1800-150'
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cookie': cookie,
                'Host': 'kissasian.sh',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', 'list-drama').find_all('div', 'item')

            try:
                for item in div:
                    url = 'https://kissasian.sh'+item.find('a')['href']
                    titleSub = item.find('a').text.strip()
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    post_two  = s.get(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    tr = soup.find('table', 'listing').find_all('tr')

                    for item in tr:
                        if item.find('td', 'episodeSub'):
                            host_url = 'https://kissasian.sh'+item.find('a')['href']+'&s=fe'
                            title = titleSub + '_' + item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'kissasian',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'philippines',
                                'cnt_writer': '',
                                'origin_url': '',
                                'origin_osp': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kissasian 크롤링 시작")
    startCrawling()
    print("kissasian 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
