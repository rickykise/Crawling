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
    i = 0;check = True; subI = 0; check_Title = ''; firstCheck = True
    link = 'https://www.tvnamu9.xyz/playlist/category_js/'+site+'/0/1?page='
    while check:
        checkSub = True
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'each-video')

        try:
            for item in div:
                url = item.find('a')['href']
                cnt_num = url.split('playlist/')[1].split('/')[0]
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
                pageUrl = 'https://www.tvnamu9.xyz/playlist/page_in_detailjs/'+cnt_num+'/'

                while checkSub:
                    subI = subI+1
                    if subI == 10:
                        subI = 0
                        checkSub=False
                    r = requests.get(pageUrl+str(subI))
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', 'each-video')

                    for item in div:
                        host_url = item.find('a')['href']
                        title = item.find('a')['title']
                        if check_Title == title:
                            subI = 0
                            firstCheck = True
                            checkSub=False;break
                        if firstCheck == True:
                            check_Title = title
                            firstCheck = False
                        title_null = titleNull(title)

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        origin_url = soup.find('div', 'content_detail').find('iframe')['src']

                        if origin_url.find('https') == -1:
                            origin_url = 'https:'+origin_url
                        origin_osp = origin_url.split('//')[1]
                        if origin_osp.find('www') != -1:
                            origin_osp = origin_osp.split('www.')[1].split('.')[0]
                        else:
                            origin_osp = origin_osp.split('.')[0]

                        data = {
                            'cnt_id': '',
                            'cnt_osp' : 'tvnamu9',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("tvnamu9 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("tvnamu9 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
