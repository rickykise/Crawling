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
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'https://m.filerun.co.kr/list.html?category1='+site+'&page='
            post_one  = s.post(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            # print(soup)
            div = soup.find_all('div', 'contents_list_box')

            try:
                for item in div:
                    cnt_chk = 0
                    title = item.find('div', 'contents_list_text_title').text.split('댓글')[0].strip()
                    title_null = titleNull(title)

                    # # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    url = 'https://m.filerun.co.kr/'+str(item['onclick']).split('../')[1].split('&category1')[0]
                    cnt_num = url.split('idx=')[1].strip()
                    cnt_writer = str(item).split('!-- |</span> ')[1].split('-->')[0].strip()
                    cnt_vol = str(item).split('|</span>')[1].split('<span')[0].strip()

                    post_two  = s.post(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')

                    cnt_price = soup.find_all('li','Content_File_2')[1].find('strike').text.split("P")[0].replace(",","").strip()
                    if soup.find_all('li','Content_File_2')[1].find('font'):
                        cnt_price = soup.find_all('li','Content_File_2')[1].find('font').text.split("P")[0].replace(",","").strip()
                    cnt_fname = soup.find('li','Content_File_3').text.strip()
                    brNum = str(soup).split('Content_File_3"')[1].split('</li')[0].count('<br/>')
                    if brNum >= 2:
                        cnt_fname = str(soup).split('class="Content_File_3">')[1].split('<br/>')[0].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filerun',
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
                    # print('=============================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_filerun 크롤링 시작")
    site = ['','MOV','DRA','MED','VOD','VOD','ANI']
    for s in site:
        startCrawling(s)
    print("m_filerun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
