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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Host': 'serieslol.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = 'https://serieslol.com/category/ซีรี่ย์เกาหลี?page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i), headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'movie')

        try:
            for item in div:
                url = item.find('a')['href']
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

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'episode')

                for item in div:
                    host_url = item.find('div', 'episode_path')['data-href']
                    if host_url.find('https:') == -1:
                        host_url = 'https:'+host_url
                    host_url = urllib.parse.unquote(host_url)
                    title = titleSub+'_'+item.find('div', 'episode_path').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'serieslol',
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
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            continue
            
if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("serieslol 크롤링 시작")
    startCrawling()
    print("serieslol 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
