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
osp_id = inspect.getfile(inspect.currentframe()).split('\\')[6].split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'http://category.tudou.com/category/c_'+site+'_a_%E9%9F%A9%E5%9B%BD_p_'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', 'td-row').find_all('div', 'td-col')

        try:
            for item in div:
                url = item.find('div', 'v-meta__title').find('a')['href']
                if url.find('https') == -1:
                    url = 'https:'+url
                titleSub = item.find('div', 'v-meta__title').find('a')['title'].replace('\\n', '').replace('\\t', '')
                title_check = titleNull(titleSub)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                if url.find('youku') != -1:
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', 'item-cover')

                    for item in div:
                        host_url = item.find('a')['href']
                        if host_url.find('https') == -1:
                            host_url = 'https:'+host_url
                        title = titleSub+'_'+item.find('a').find('div', 'title').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'tudou',
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
                elif url.find('tudou') != -1:
                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', 'td-listbox__list__item--show')

                    for item in div:
                        host_url = 'https://video.tudou.com/v/'+item['data-vid']
                        title = titleSub + '_' + item.find('div', 'td-video__meta__title').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'tudou',
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
                else:
                    continue
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tudou 크롤링 시작")
    site = ['97','85','96']
    for s in site:
        startCrawling(s)
    print("tudou 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
