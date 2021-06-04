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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': 'tokenId=t_pmufc6rlyq5c; popundr=1; tokenId=t_iq52kj5mm6sd; ppu_main_65aa283021630dfd9030555c4c61a78c=1; cf_chl_prog=a21; dom3ic8zudi28v8lr6fgphwffqoz0j6c=17ae7c1f-a356-457c-97d5-597d532f4909%3A1%3A2; cf_chl_1=89f19288c70fdb6; ppu_main_70e9836d3a3b8c9a0f339945ba4bd257=1; ppu_sub_65aa283021630dfd9030555c4c61a78c=1; 494668b4c0ef4d25bda4e75c27de2817=17ae7c1f-a356-457c-97d5-597d532f4909:1:2; _gid=GA1.2.1867548124.1596159241; _ga=GA1.2.388544304.1596159241; cf_clearance=788e89d8f15e422aa451402cb619c0ebbd421155-1596159230-0-1zbd7818d9z4ca45cc9zf27a066e-250',
    'Host': 'www.kseries.io',
    'If-Modified-Since': 'Fri, 31 Jul 2020 01:11:07 GMT',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = "https://www.kseries.io/kseries/page/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find('div', id='archive-content').find_all('article', id=re.compile("post-+"))

        try:
            for item in article:
                url = item.find('div', 'data').find('a')['href']
                titleSub = item.find('div', 'data').find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find_all('ul', 'episodios')[1].find_all('li')

                for item in li:
                    host_url = item.find('a')['href']
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'kseries.io',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("kseries.io 크롤링 시작")
    startCrawling()
    print("kseries.io 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
