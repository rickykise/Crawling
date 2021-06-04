import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = "http://m.fileguri.com/index.php?mode=content&cate="+site+"&adult_not=y&curr_page="+str(i)
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find('div', 'cont_txtlist')
            li = div.find('ul').find_all('li')
            try:
                for item in li:
                    cnt_chk = 0
                    cnt_num = item.find('a', 'txtlink')['href'].split('idx=')[1].split('&')[0]
                    url = 'http://m.fileguri.com/index.php' + item.find('a', 'txtlink')['href']
                    text = str(item)
                    cnt_vol = text.split("class='cost'>")[1].split("</span>")[0].strip()
                    cnt_price = item.find('span', 'cost').text.strip().replace(",","").split('P')[0]
                    cnt_writer = item.find_all('span', 'greyfont')[1].text.strip()
                    if item.find('span', 'bullet icon_img'):
                        cnt_chk = 1

                    post_two  = s.post(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    div = soup.find('div', id='cont_detail')

                    if soup.find('div', 'ctvInterestLInk'):
                        titlediv = soup.find('div', 'ctvInterestLInk').text.strip()
                        title = soup.find('div', 'detailtitle').text.replace('\n', '').split(titlediv)[0].strip()
                    else:
                        title = soup.find('div', 'detailtitle').text.replace('\n', '').strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    # checkPrice = str(keyCheck['p'])
                    # if checkPrice == cnt_price:
                    #     cnt_chk = 1
                    cnt_fname = soup.find('div', id='filelistBox').find('dt').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileguri',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_fileguri 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_fileguri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
