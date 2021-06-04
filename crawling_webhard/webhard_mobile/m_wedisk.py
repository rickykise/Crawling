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
    'Content-Type': 'application/x-www-form-urlencoded',
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
            link = 'https://m.wedisk.co.kr/mobile/mobile_list.jsp?vp='+str(i)+'&sect='+site+'&s_sub=&file_type=&max_vir_id=80927456&group_cd='
            post_one  = s.post(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', 'nlList')
            div = soup.find_all('div', onclick=re.compile("contentView+"))

            try:
                for item in div:
                    adult = item['onclick'].split("', '")[1].split("',")[0]
                    if adult == 'Y':
                        continue
                    cnt_num = item['onclick'].split('contentView(')[1].split(',')[0]
                    url = 'https://m.wedisk.co.kr/mobile/contents_view.jsp?id='+cnt_num+'&strm_id=null'
                    title = item.find('div', 'titie').text.strip()
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    cnt_writer = item.find('div', 'contInfo').text.split('/')[2].strip()
                    price = item.find('span', 'contentCash').text.strip()
                    cnt_chk = 0
                    if price.find('캐시') != -1:
                        cnt_price = item.find('span', 'contentCash').text.split('캐시')[0].replace(",","").strip()
                    else:
                        cnt_price = item.find('span', 'contentCash').text.split('(')[0].replace(",","").strip()
                        cnt_chk = 1

                    post_two  = s.post(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')

                    cnt_vol = soup.find('div', 'list_title').find('span').text.split('/')[1].split('/')[0].strip()
                    fname = soup.find('li', 'info_title').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'wedisk',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_wedisk 크롤링 시작")
    site = ['','01','02','03','05']
    for s in site:
        startCrawling(s)
    print("m_wedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
