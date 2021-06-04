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
    link = site[0]
    end = site[1]
    while check:
        i = i+1
        if i == end:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'v_con_box').find_all('li')

        try:
            for item in li:
                url = 'https://www.bo3.net'+item.find('p', 'v-tit').find('a')['href']
                titleSub = item.find('p', 'v-tit').find('a').text.strip()
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
                ul = soup.find_all('ul', 'play_num_list')

                for item in ul:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'https://www.bo3.net'+item.find('a')['href']
                        title = titleSub + '_' + item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'bo3.net',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
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

    print("bo3.net 크롤링 시작")
    site = [('https://www.bo3.net/list/rihanju/area/%E9%9F%A9%E5%9B%BD/lang/%E9%9F%A9%E8%AF%AD/page/{}.html',6),('https://www.bo3.net/list/zongyi/area/%E9%9F%A9%E5%9B%BD/lang/%E9%9F%A9%E8%AF%AD/page/{}.html',8)]
    for item in site:
        startCrawling(item)
    print("bo3.net 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
