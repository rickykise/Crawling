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
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'showq.tv',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True;cnt_osp = ''
    if site.find('showq') != -1:
        cnt_osp = "showq.tv"
    else:
        cnt_osp = 'chinaq'
    link = site+'/kr/'
    while check:
        i = i+1
        if i == 2:
            break
        r = requests.get(link, headers=headers)
        print(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'drama_rich').find_all('a')

        # try:
        for item in li:
            url = site+item['href']
            titleSub = item.text.strip()
            title_check = titleNull(titleSub)

            # 키워드 체크
            getKey = getKeyword()
            keyCheck = checkTitle(title_check, getKey)
            if keyCheck['m'] == None:
                continue
            cnt_id = keyCheck['i']
            cnt_keyword = keyCheck['k']

            r = requests.get(url, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('ul', 'sizing'):
                li = soup.find('ul', 'sizing').find_all('li')

                for item in li:
                    host_url = site+item.find('a')['href']
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : cnt_osp,
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
            else:
                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : cnt_osp,
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'china',
                    'cnt_writer': ''
                }
                print(data)
                print("=================================")

                # dbResult = insertALL(data)

        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("showq.tv 크롤링 시작")
    site = ['https://showq.tv','https://chinaq.me']
    for s in site:
        startCrawling(s)
    print("showq.tv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
