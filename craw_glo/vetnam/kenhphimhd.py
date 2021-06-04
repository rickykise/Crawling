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
    'Connection': 'Keep-Alive',
    'Cookie': '__cfduid=d433690d8f0b245b927cc45fd3e5085021574323775; _ga=GA1.2.120308999.1574323777; _gid=GA1.2.413940164.1574323777; AdskeeperStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A11%2C%22TejndEEDj%22%3A%22NaxDorM7d%22%7D%2C%22C259293%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323778468%7D%2C%22C259287%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323779132%7D%2C%22C259291%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323779121%7D%2C%22C259289%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323778892%7D%2C%22C259286%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323778929%7D%2C%22C259283%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323778975%7D%2C%22C259290%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323779038%7D%2C%22C259292%22%3A%7B%22page%22%3A1%2C%22time%22%3A1574323779085%7D%7D',
    'Host': 'kenhphimhd.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = 'http://kenhphimhd.com/quoc-gia-han-quoc-9.a13i'
    link2 = '.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        sub = soup.find_all('a', 'movie-link')

        try:
            for item in sub:
                url = 'http://kenhphimhd.com'+item['href']
                titleSub = item['title']
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
                url2 = 'http://kenhphimhd.com'+soup.find('a', id='btn-film-watch')['href']

                r = requests.get(url2, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'list-episode').find_all('li', 'episode')

                for item in li:
                    host_url = 'http://kenhphimhd.com'+item.find('a')['href']
                    titleNum = item.find('a').text.strip()
                    title = titleSub+'_'+titleNum
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'kenhphimhd',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
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

    print("kenhphimhd 크롤링 시작")
    startCrawling()
    print("kenhphimhd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
