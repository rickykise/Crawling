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
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True;rcheck = True;
    link = 'https://kissasian.sh/Country/South-Korea?page='
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 30:
                break
            cookie = '_ga=GA1.2.138393301.1579057847; __cfduid=d9ee16af47dec09f7e16984fb7a3df1c71579058225; cf_clearance=d4724b11ee191c991efa82d94b59d0b98e60c443-1581578451-0-150; _gid=GA1.2.224987006.1581578454; ppu_main_c0c197ad1929d1daa75380313517e39d=1; psu_main_33739c336432ac00a30175408abb6640=1; dom3ic8zudi28v8lr6fgphwffqoz0j6c=9a99f5c0-e579-42f3-ba65-64de85e10ec4%3A1%3A2; 494668b4c0ef4d25bda4e75c27de2817=9a99f5c0-e579-42f3-ba65-64de85e10ec4:1:2'
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cookie': cookie,
                'Host': 'kissasian.sh',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            post_one  = s.post(link+str(i), headers=headers)
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
