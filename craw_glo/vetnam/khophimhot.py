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
    i = 0;a = 1;check = True
    link = 'https://khophimhot.net/phim-han-quoc/trang-'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+'.html')
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'last-film-box').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                title1 = item.find('span', 'movie-title-1').text.strip()
                if title1.find('(') != -1:
                    title1 = title1.split('(')[0].strip()
                title2 = item.find('span', 'movie-title-2').text.strip()
                if title2.find('(') != -1:
                    title2 = title2.split('(')[0].strip()
                titleSub = title1+'_'+title2
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
                url2 = soup.find('a', 'btn-danger')['href']

                r = requests.get(url2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                ul = soup.find_all('ul', 'list-episode')

                for item in ul:
                    li = item.find_all('li')
                    for item in li:
                        host_url = item.find('a')['href']
                        title = titleSub + '_' + item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'khophimhot',
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

    print("khophimhot 크롤링 시작")
    startCrawling()
    print("khophimhot 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
