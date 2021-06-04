import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.4399d.com/hanguoju/index{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i) if i > 1 else ''))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        li = soup.find('div',  id='tj-list').find_all('li',  'item')

        try:
            for item in li:
                url = 'https://www.4399d.com'+item.find('a')['href']
                titleSub = item.find('div', 'detail').find('span', 's1').text.strip()
                title_null = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(titleSub,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                sub = soup.find('div',  'top-list-ji').find_all('a', href=lambda x: x and "/video/?" in x)

                for item in sub:
                    host_url = 'https://www.4399d.com'+item['href']
                    title = titleSub+'_'+item['title']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': '4399d',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'other',
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

    print("4399d 크롤링 시작")
    site = ['drama',  'entertainment',  'fin']
    for s in site:
        startCrawling(s)
    print("4399d 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
