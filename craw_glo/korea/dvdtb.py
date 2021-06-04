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
    'Connection': 'Keep-Alive',
    'Cookie': '__cfduid=d9d2ac6cde334b71154a4b04c532443311573806541; 2a0d2363701f23f8a75028924a3af643=NjEuODIuMTEzLjE5Ng%3D%3D',
    'Host': 'dvdtb.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'http://dvdtb.com/'+site+'.php?&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'list-group').find_all('li', 'list-group-item')

        try:
            for item in li:
                url = 'http://dvdtb.com/'+item.find('a')['href']
                title = item.find('a').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                origin_url = soup.find('iframe')['src']

                if origin_url.find('https') == -1:
                    origin_url = 'https:'+origin_url
                origin_osp = origin_url.split('//')[1]
                if origin_osp.find('www') != -1:
                    origin_osp = origin_osp.split('www.')[1].split('.')[0]
                else:
                    origin_osp = origin_osp.split('.')[0]

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'dvdtb',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'southkorea',
                    'cnt_writer': '',
                    'origin_url': origin_url,
                    'origin_osp': origin_osp
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dvdtb 크롤링 시작")
    site = ['drama', 'ent']
    for s in site:
        startCrawling(s)
    print("dvdtb 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
