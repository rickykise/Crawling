import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'http://feifany.cc/index.php/vod/show/area/%E9%9F%A9%E5%9B%BD/id/15/page/{}.html'
    while check:
        i = i+1
        if i == 16:
            break
        r = requests.get(link.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'stui-vodlist').find_all('li')

        try:
            for item in li:
                url = 'http://feifany.cc'+item.find('a')['href']
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
                div = soup.find_all('div', 'stui-pannel')

                for item in div:
                    if item.find('ul', 'stui-content__playlist'):
                        li = soup.find('ul', 'stui-content__playlist').find_all('li')
                        for item in li:
                            host_url = 'http://feifany.cc'+item.find('a')['href']
                            title = titleSub + '_' + item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'feifany.cc',
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

    print("feifany.cc 크롤링 시작")
    startCrawling()
    print("feifany.cc 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
