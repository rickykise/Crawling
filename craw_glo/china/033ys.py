import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(craw):
    i = 0;check = True
    while check:
        i = i+1
        if i == craw['end']:
            break
        r = requests.get(craw['link'].format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li','vodlist_item')
        try:
            for item in li:
                url = 'https://www.033ys.cc'+item.find('a')['href']
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
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                playbtn = soup.find('div', 'playbtn').find('a')
               
                r = requests.get('https://www.033ys.cc'+playbtn['href'])
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('ul', 'content_playlist').find_all('a',href=lambda x: x and "/vodplay/" in x)

                for item in sub:
                    host_url = 'https://www.033ys.cc'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '033ys',
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
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("033ys 크롤링 시작")
    site = [{'link':'https://www.033ys.cc/vodshow/15-%E9%9F%A9%E5%9B%BD-------{}---.html','end':16},{'link':'https://www.033ys.cc/vodshow/3--------{}---.html','end':36}]
    for item in site:
        startCrawling(item)
    print("033ys 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
