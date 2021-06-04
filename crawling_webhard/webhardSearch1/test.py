
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

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 10:
                break
            if site == '':
                link = 'https://filerun.co.kr/contents/index.htm?category1=&category2=&groupcate=&s_column=&s_word=&rows=20&show_type=&page='
                post_one  = s.get(link+str(i))
            else:
                link = 'https://filerun.co.kr/contents/?category1='+site+'&category2=&groupcate=&s_column=&s_word=&rows=20&show_type=0&page='
                post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            li = soup.find_all('tr', 'reply')

            try:
                for item in li:
                    if item.find('script'):
                        continue
                    # cnt_num = item.find('input')['value']
                    # url = 'http://filerun.co.kr/contents/view.htm?idx='+cnt_num
                    url = 'http://filerun.co.kr/contents/warning.htm?idx=249117'
                    cnt_num = '249117'
                    url2 = 'http://filerun.co.kr/contents/view_top.html?idx='+cnt_num
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('filerun',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('filerun',title,title_null,url)
                    #     continue

                    # cnt_chk = 0
                    # cnt_vol = item.find('td', 'date1').text.strip()
                    # cnt_writer = str(item).split(';">')[1].split('</a')[0].strip()
                    # cnt_price = item.find_all('td', 'date1')[1].find('strike').text.replace(",","").replace('\h','').split("P")[0].strip()
                    # if item.find_all('td', 'date1')[1].find('font'):
                    #     cnt_price = item.find_all('td', 'date1')[1].find('font').text.replace(",","").split("P")[0].strip()

                    post_two  = s.get(url2)
                    soup = bs(post_two.text, 'html.parser')
                    print(soup)
                    print("=================================")

                    # cnt_fname = soup.find('span', 'font_layerlist').text.strip()
                    # if cnt_fname == '/':
                    #     cnt_fname = soup.find_all('span', 'font_layerlist')[1].text.strip()
                    #
                    # data = {
                    #     'Cnt_num' : cnt_num,
                    #     'Cnt_osp' : 'filerun',
                    #     'Cnt_title': title,
                    #     'Cnt_title_null': title_null,
                    #     'Cnt_url': url,
                    #     'Cnt_price': cnt_price,
                    #     'Cnt_writer' : cnt_writer,
                    #     'Cnt_vol' : cnt_vol,
                    #     'Cnt_fname' : cnt_fname,
                    #     'Cnt_chk': cnt_chk
                    # }
                    # # print(data)
                    # # print("=================================")
                    #
                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filerun 크롤링 시작")
    site = ['','MOV','DRA','MED','MED','VOD','ANI']
    for s in site:
        startCrawling(s)
    print("filerun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
