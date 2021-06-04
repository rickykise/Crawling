import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

LOGIN_INFO = {
    'rurl': 'http://www.totodisk.com/content/index.toto?itemcode=713346',
    'target': '',
    'userId': 'up0002',
    'userPwd': 'up000123'
}

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('https://member.totodisk.com/login/login', data=LOGIN_INFO)
        while check:
            i = i+1
            if i == 5:
                break
            link = 'http://www.totodisk.com/tv/list/getAjaxTvListImage.toto?pagesize=10&page='+str(i)+'&type=list&genre=000000&channel=04050'+site+'&sectioncode='
            post_one  = s.get(link)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('table').find_all('tr')

            # try:
            for item in tr:
                if item.find('td'):
                    url = 'http://www.totodisk.com'+item.find('a')['href'].replace('amp;', '')
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeywordNet()
                    keyCheck = checkTitleNet(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('totodisk',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('totodisk',title,title_null,url)
                    #     continue
                    checkPrice = str(keyCheck['p'])

                    post_two  = s.get(url)
                    soup = bs(post_two.text, 'html.parser')
                    tr2 = soup.find('div', 'movie_list04').find('table').find_all('tr')
                    cnt_chk = 0

                    for item in tr2:
                        if item.find('td'):
                            text = item.find('td').text.strip()
                            if text.find('방송이 없습니다') != -1:
                                continue
                            url = item.find('a')['href']
                            cnt_num = url.split('itemcode=')[1]
                            title = item.find('a').text.strip()
                            title_null = titleNull(title)
                            cnt_price = item.find('td', 'taR').text.split("원")[0].strip().replace(',', '')
                            cnt_writer = ''
                            if checkPrice == cnt_price or cnt_price == '500' or cnt_price == '700' or cnt_price == '1000' or cnt_price >= '1500':
                                cnt_chk = 1

                            post_th  = s.get(url)
                            soup = bs(post_th.text, 'html.parser')
                            cnt_fname = soup.find_all('table')[1].find('td').text.strip()
                            cnt_vol = soup.find_all('table')[1].find_all('td')[1].text.strip().replace(' ', '')

                            data = {
                                'Cnt_num' : cnt_num,
                                'Cnt_osp' : 'totodisk',
                                'Cnt_title': title,
                                'Cnt_title_null': title_null,
                                'Cnt_url': url,
                                'Cnt_price': cnt_price,
                                'Cnt_writer' : cnt_writer,
                                'Cnt_vol' : cnt_vol,
                                'Cnt_fname' : cnt_fname,
                                'Cnt_chk': cnt_chk
                            }
                            print(data)
                            print("=================================")

                                # dbResult = insertALL(data)
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("totodisk 크롤링 시작")
    site = ['1','3','6','2','4']
    for s in site:
        startCrawling(s)
    print("totodisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
