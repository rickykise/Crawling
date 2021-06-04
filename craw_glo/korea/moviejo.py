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
path = inspect.getfile(inspect.currentframe())
x = path.split('\\')
x.reverse()
osp_id = x[0].split('.py')[0].strip()

def startCrawling(site):
    i = 0;check = True;cnt_osp = 'moviejo'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'bbs/board.php?bo_table='+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://z27.moviejo.net/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('ul', 'fz_list').find_all('div', 'fz_subject')

        try:
            for item in div:
                if item.find('a'):
                    url = item.find('a')['href']
                    if url.find('&page') != -1:
                        url = url.split('&page')[0].strip()
                    url = urllib.parse.unquote(url)
                    titleSub = item.find('a').text.strip()
                    if titleSub.find('새글') != -1:
                        titleSub = titleSub.split('새글')[0].strip()
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
                    ul = soup.find_all('ul', re.compile("link-+"))

                    for item in ul:
                        sub = item.find_all('a')
                        for item in sub:
                            host_url = item['href']
                            title = titleSub+'_'+item.text.strip()
                            if title.find('다운로드') != -1:
                                continue
                            title_null = titleNull(title)

                            origin_url = host_url
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('ww') != -1:
                                origin_osp = origin_osp.split('.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : cnt_osp,
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

    print("moviejo 크롤링 시작")
    site = ['entertainment', 'drama']
    for s in site:
        startCrawling(s)
    print("moviejo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
