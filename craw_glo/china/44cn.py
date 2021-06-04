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
                url = 'https://www.44cn.net'+item.find('a')['href']
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
                sub = soup.find('div', 'play_list_box').find_all('a')

                for item in sub:
                    host_url = 'https://www.44cn.net'+item['href']
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : '44cn',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("44cn 크롤링 시작")
    site = [{'link':'https://www.44cn.net/vodshow/15/area/%E9%9F%A9%E5%9B%BD/page/{}.html','end':20},{'link':'https://www.44cn.net/vodshow/3/area/%E6%97%A5%E9%9F%A9/page/{}.html','end':4}]
    for item in site:
        startCrawling(item)
    print("44cn 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
