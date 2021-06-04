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
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'index-area').find('ul').find_all('li', 'p1')

        try:
            for item in li:
                url = 'https://9xigua.com'+item.find('a')['href']
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
                div = soup.find_all('div', id=re.compile("vlink_+"))

                for item in div:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'https://www.9xigua.com'+item.find('a')['href']
                        title = titleSub + '_' + item.find('a')['title']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '9xigua',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
                            'cnt_writer': '',
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("9xigua 크롤링 시작")
    site = [{'link':'https://9xigua.com/vod-type-id-15-page-{}.html','end':30},{'link':'https://9xigua.com/vod-type-id-34-page-{}.html','end':16}]
    for item in site:
        startCrawling(item)
    print("9xigua 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
