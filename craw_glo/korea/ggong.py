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

def startCrawling(site):
    i = 0;check = True
    site = urllib.parse.quote(site)
    link = 'https://www.ggong.live/'+site+'/'
    while check:
        i = i+1
        if i == 30:
            break
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cookie': '_ga=GA1.2.1878359774.1573802157; __cfduid=d93d6cce115ffe2f4691e9bbd6f86899f1573802151',
            'Host': 'www.ggong.live',
            'Referer': 'https://www.ggong.live/'+site,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'XMLHttpRequest': 'XMLHttpRequest'
        }
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'col-sm-4')

        try:
            for item in div:
                url_check = item.find('a')['href']
                if url_check.find('CONTACT') != -1:
                    continue
                url = 'https://www.ggong.live'+item.find('a')['href']
                titleSub = item.find('a')['title']
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
                tr = soup.find('div', 'col').find_all('tr')

                for item in tr:
                    title = titleSub+'_'+item.find('td').text.strip()
                    title_null = titleNull(title)
                    sub = item.find_all('a')
                    for item in sub:
                        host_url = item['href']
                        origin_url = host_url

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'ggong',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
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

    print("ggong 크롤링 시작")
    site = ['TV/드라마', 'TV/예능', '애니메이션', 'TV/영화']
    for s in site:
        startCrawling(s)
    print("ggong 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
