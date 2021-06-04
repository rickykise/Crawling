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
    i = 0;check = True;a = 0;checkA = True;cnt_osp = 't30.etvlink'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+'bbs/board.php?bo_table='+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://t30.etvlink.com/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        td = soup.find_all('td', 'fz_subject')

        try:
            if site == "dramakor":
                for item in td:
                    url = item.find('a')['href']+'&page='
                    url = urllib.parse.unquote(url)
                    titleSub = item.find('a').text.strip()
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    while checkA:
                        a = a+1
                        if a == 10:
                            break
                        r = requests.get(url+str(a))
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        td2 = soup.find_all('td', 'fz_subject')
                        if len(td2) < 1:
                            checkA = False;break

                        for item in td2:
                            url2 = item.find_all('a')[1]['href']
                            url2 = urllib.parse.unquote(url2)
                            title = item.find_all('a')[1].text.strip()
                            if title.find('★') != -1:
                                title = title.split('★')[0].strip()
                            title_null = titleNull(titleSub)

                            r = requests.get(url2)
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")
                            div = soup.find_all('div', id='vmega')

                            for item in div:
                                host_url = item.find('a')['href']

                                data = {
                                    'cnt_id': cnt_id,
                                    'cnt_osp' : cnt_osp,
                                    'cnt_title': title,
                                    'cnt_title_null': title_null,
                                    'host_url' : host_url,
                                    'host_cnt': '1',
                                    'site_url': host_url,
                                    'cnt_cp_id': 'sbscp',
                                    'cnt_keyword': cnt_keyword,
                                    'cnt_nat': 'southkorea',
                                    'cnt_writer': ''
                                }
                                # print(data)
                                # print("=================================")

                                dbResult = insertALL(data)

            else:
                for item in td:
                    url = item.find('a')['href']
                    url = urllib.parse.unquote(url)
                    title = item.find('a').text.strip()
                    if title.find('★') != -1:
                        title = title.split('★')[0].strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', id='vmega')

                    for item in div:
                        host_url = item.find('a')['href']

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : cnt_osp,
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': host_url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)

        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("t30.etvlink 크롤링 시작")
    site = ['dramakor', 'enter']
    for s in site:
        startCrawling(s)
    print("t30.etvlink 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
