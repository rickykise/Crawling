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

def startCrawling(link):
    i = 0;check = True

    while check:
        i = i+1
        if i == 30:
            break
        if link.find('vod-list-id') == -1:
            if i == 1:
                r = requests.get(link.format('.html'))
            else:
                r = requests.get(link.format('-'+str(i)+'.html'))
        else:
            if i == 1:
                r = requests.get(link.format(''))
            else:
                r = requests.get(link.format('-pg-'+str(i)))
        
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'index-area').find('ul').find_all('li', 'p1')

        try:
            for item in li:
                url = 'https://www.xkdy888.com'+item.find('a')['href']
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
                        host_url = 'https://www.xkdy888.com'+item.find('a')['href']
                        title = titleSub + '_' + item.find('a')['title']
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'xkdy888',
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

    print("xkdy888 크롤링 시작")

    link = ['https://www.xkdy888.com/vodtypehtml/14/index{}','https://www.xkdy888.com/index.php?m=vod-list-id-3{}-order--by--class-0-year-0-letter--area-%E9%9F%A9%E5%9B%BD-lang-.html']
    for url in link:
        startCrawling(url)
    print("xkdy888 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
