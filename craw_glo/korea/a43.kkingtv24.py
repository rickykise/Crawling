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

def startCrawling(site):
    i = 0;check = True
    link = 'http://a43.kkingtv24.com/home1?c='+site+'&s=0&f=0&p='
    while check:
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        i = i+1
        div = soup.find_all('div', 'medProgram_link')

        try:
            for item in div:
                url = 'http://a43.kkingtv24.com'+item.find('a')['href']
                title = item.find('a').find('div').text.strip().replace('\n', '')
                if title.find('/기타') != -1:
                    continue
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'medProgram')

                for item in div:
                    host_url = 'http://a43.kkingtv24.com'+item.find('a')['href']
                    title = item.find('a').find('div').text.strip().replace('\n', '')
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    xNum = str(soup).split(", ['")[1].split("',")[0]
                    host_url = 'http://a43.kkingtv24.com/a03?d=0&a=1&c=0&n=0&x='+xNum

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    hostText = str(soup)
                    host_url = hostText.split('replace("')[1].split('")')[0]

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    origin_url = soup.find_all('iframe')[1]['src']

                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'a43.kkingtv24',
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

    print("a43.kkingtv24 크롤링 시작")
    site = ['0', '1', '2']
    for s in site:
        startCrawling(s)
    print("a43.kkingtv24 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
