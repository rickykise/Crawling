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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'https://mtfuck.com/vod1/p'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'board-gallery').find_all('div', 'gallery-item')

        try:
            for item in li:
                url = item.find('div', 'gallery-item-info').find('h4').find('a')['href'].split('?page')[0]
                title = item.find('div', 'gallery-item-info').find('h4').find('a').text.strip()
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find_all('a', rel='nofollow noreferrer noopener')

                for item in sub:
                    cnt_text = item.text.strip()
                    if cnt_text.find('다시보기') != -1:
                        host_url = item['href']

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'mtfuck',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
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

    print("mtfuck 크롤링 시작")
    startCrawling()
    print("mtfuck 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
