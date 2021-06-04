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

def startCrawling():
    i = 0;check = True
    while check:
        i = i+1
        if i == 15:
            break
        r = requests.get('http://www.172.ink/index.php/vod/show/area/%E9%9F%A9%E5%9B%BD/id/15/lang/%E9%9F%A9%E8%AF%AD/page/{}/'.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li','vodlist_item')
        try:
            for item in li:
                url = 'http://www.172.ink'+item.find('a')['href']
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
               
                r = requests.get('http://www.172.ink'+playbtn['href'])
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('ul', 'content_playlist').find_all('a',href=lambda x: x and "/vod/play/" in x)

                for item in sub:
                    host_url = 'http://www.172.ink'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '172.ink',
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

    print("172.ink 크롤링 시작")
    startCrawling()
    print("172.ink 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
