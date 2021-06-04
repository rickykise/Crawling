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
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)


def startCrawling():
    i = 0;check = True
    link = "http://www2.fastdrama.me/browse/korean/dramas/all/all/all/0/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'grid').find_all('div', 'v-grid')

        try:
            for item in div:
                url = 'http://www2.fastdrama.me'+item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                print(keyCheck['m'])

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'list-eps')
                for item in div:
                    host_url = 'http://www2.fastdrama.me'+item.find('a')['href']
                    if host_url.find('javascript') != -1:
                        continue
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'fastdrama',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    print(data)
                    print('==============================')

                    # dbResult = insertALL(data)

                    # r = requests.get(host_url)
                    # c = r.content
                    # soup = BeautifulSoup(c,"html.parser")
                    # server_url = soup.find('iframe', id='videoembed')['src']
                    # headers = {
                    #     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    #     'Accept-Encoding': 'gzip, deflate',
                    #     'Accept-Language': 'ko-KR',
                    #     'Connection': 'Keep-Alive',
                    #     'Host': 'www1.fastdrama.me',
                    #     'Referer': host_url,
                    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                    # }
                    # sys.setrecursionlimit (2000)
                    #
                    # with requests.Session() as s:
                    #     post_one  = s.get(server_url, headers=headers)
                    #     soup = bs(post_one.text, 'html.parser')
                    #     host_cnt = len(soup.find_all('input', id='btnLink@i'))
                    #
                    #     data = {
                    #         'cnt_id': cnt_id,
                    #         'cnt_osp' : 'fastdrama',
                    #         'cnt_title': title,
                    #         'cnt_title_null': title_null,
                    #         'host_url' : host_url,
                    #         'host_cnt': '1',
                    #         'site_url': url,
                    #         'cnt_cp_id': 'sbscp',
                    #         'cnt_keyword': cnt_keyword,
                    #         'cnt_nat': 'thailand',
                    #         'cnt_writer': ''
                    #     }
                    #     # print(data)
                    #     # print("=================================")
                    #
                    #     dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("fastdrama 크롤링 시작")
    startCrawling()
    print("fastdrama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
