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
    i = 0;check = True
    link = 'https://rapphim18.com/quoc-gia/kr/trang-'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cookie': '__cfduid=d1ab17cdc491d00308204c068b098f0261615535775; PHPSESSID=6hhpufsaak1e6cfupg4ket5uq8; _ga_Z8T2NM9XJ9=GS1.1.1615535777.1.0.1615535780.0; _ga=GA1.2.1472519433.1615535777; _gid=GA1.2.1150595067.1615535777; _gat_gtag_UA_129054687_1=1; adpia_popup_p1m1=1',
            'Host': 'rapphim18.com',
            'Referer': link+str(i)+link2,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'list-film').find_all('div', 'item')

        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
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
                url2 = soup.find('div', 'watch').find('a')['href']

                r = requests.get(url2, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('div', 'episodes').find('ul').find_all('li')

                for item in li:
                    host_url = 'https://rapphim18.com'+item.find('a')['href']
                    cnt_num = item.find('a')['id']
                    titleNum = item.find('a').text.strip()
                    if titleNum.find('Full') != -1:
                        title = titleSub
                    else:
                        title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'rapphim18',
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

    print("rapphim18 크롤링 시작")
    startCrawling()
    print("rapphim18 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
