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
    i = 0;check = True;cnt_osp = 'v1.sonagitv'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        link = group_url+site+'/page/'
        cnt_osp = group_id
    else:
        link = 'https://v1.sonagitv.xyz/'+site+'/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div', id=re.compile("pagebuilder-+")).find_all('div', 'item')

        try:
            for item in div:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                title = item.find('a')['title']
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
                host_url = soup.find('div', 'embed-responsive').find('a')['href']
                host_url = urllib.parse.unquote(host_url)

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
                    'cnt_writer': ''
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)

                if site != 'movie':
                    div2 = soup.find('div', 'carousel-inner').find_all('div', 'col-md-3')

                    for item in div2:
                        url = item.find('a')['href']
                        url = urllib.parse.unquote(url)
                        title = item.find('h3').find('a').text.strip()
                        title_null = titleNull(title)

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        host_url = soup.find('div', 'embed-responsive').find('a')['href']
                        host_url = urllib.parse.unquote(host_url)

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
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("v1.sonagitv 크롤링 시작")
    site = ['entertainment', 'drama', 'endkdrama', 'movie']
    for s in site:
        startCrawling(s)
    print("v1.sonagitv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
