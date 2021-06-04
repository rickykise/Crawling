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

def startCrawling():
    i = 0;check = True
    link = 'https://dongphym.net/content/search?t=ft&nt=KR&mt=tvshow&p='
    while check:
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'flex-wrap-movielist').find_all('a', 'movie-item')
        i = i+1

        try:
            for item in div:
                url = item['href']
                titleSub = item.find('h6').text.strip()
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
                div2 = soup.find('div', 'movie-eps-all').find_all('a', 'movie-eps-item')

                for item in div2:
                    host_url = item['href']
                    if host_url.find('https') == -1:
                        host_url = 'https://dongphym.net'+item['href']
                    if host_url == '#':
                        continue
                    title = titleSub + '_' + item.text.split('Tập')[1].strip()
                    title_null = titleNull(title)


                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'dongphym',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
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

    print("dongphym 크롤링 시작")
    startCrawling()
    print("dongphym 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
