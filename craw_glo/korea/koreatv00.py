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
    link = 'http://www.koreatv00.com/board/g-a-'+site+'?&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'gallery-box')

        try:
            for item in div:
                url = item.find('a')['href']
                if url.find('&page=') != -1:
                    url = url.split('?&page')[0]
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']


                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Connection': 'Keep-Alive',
                    'Host': 'www.koreatv00.com',
                    'Referer': url,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                key = str(soup).split('var key_val	=')[1].split(';')[0].replace('"', '').strip()
                tr = soup.find('div', 'contents-view').find_all('tr')


                for item in tr:
                    if item.find('button'):
                        sid = item.find('button')['data-sid']
                        stype = item.find('button')['linktype']
                        host_url = 'http://www.koreatv00.com/postact/getlink?sid='+sid+'&stype='+stype+'&key='+key
                        title = titleSub+'_'+item.find('td').text.strip()
                        title_null = titleNull(title)

                        # Data = {
                        #     'key': key,
                        #     'sid': sid,
                        #     'stype': stype
                        # }
                        #
                        # r = requests.get(host_url, headers=headers, data=Data)
                        # c = r.content
                        # soup = BeautifulSoup(c,"html.parser")

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'koreatv00',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': '',
                            'origin_url': '',
                            'origin_osp': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("koreatv00 크롤링 시작")
    site = ['3','2']
    for s in site:
        startCrawling(s)
    print("koreatv00 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
