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

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'coids': '',
                'ct_id': '000'+site,
                'eName': site,
                'e_s': '',
                'noncpYN': '',
                'p_page': i,
                's_field': '3',
                'searchWord': '',
                'sortF': ''
            }
            link = 'http://m.bigfile.co.kr/bm/contents/ajax.list.php'
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            li = soup.find_all('li')
            try:
                for item in li:
                    adult = item.find('a')['href']
                    if adult.find('/bm/account/loginAp.php') != -1:
                        continue
                    cnt_num = item.find('a')['href'].split("co_id=")[1].split("','")[0]
                    url = 'http://m.bigfile.co.kr' + item.find('a')['href'].split("','")[2].split("','")[0]
                    cnt_vol = item.find('span', 'txt_info3').text.strip()
                    cnt_price = item.find('span', 'txt_info').text.strip().split(cnt_vol)[1].split("캐시")[0].replace(",","")
                    cnt_writer = item.find('span', 'txt_info2').text.strip()

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    cnt_chk = 0

                    if soup.find('div', 'tit_view').find('span', 'bt_cp'):
                        span = soup.find('div', 'tit_view').find('span', 'bt_cp').text.strip()
                        title = soup.find('div', 'tit_view').text.replace('\xa0', '').split(span)[1].strip()
                        cnt_chk = 1
                    else:
                        title = soup.find('div', 'tit_view').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    span2 = soup.find('div', 'file_info_view').find('li').find('span').text.strip()
                    cnt_fname = soup.find('div', 'file_info_view').find('li').text.split(span2)[0].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'bigfile',
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

    print("m_bigfile 크롤링 시작")
    site = ['','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("m_bigfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
