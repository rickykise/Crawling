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

def startCrawling(key):
    print('키워드: '+key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            link = "https://filerun.co.kr/contents/?category1=&category2=&groupcate=&s_column=title&s_word="+encText+"&rows=20&show_type=0&page="
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            li = soup.find_all('tr', 'reply')
            if len(li) <= 2:
                break

            try:
                for item in li:
                    if item.find('script'):
                        continue
                    cnt_num = item.find('input')['value']
                    url = 'https://filerun.co.kr/contents/view.htm?idx='+cnt_num
                    url2 = 'https://filerun.co.kr/contents/view_top.html?idx='+cnt_num
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filerun',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filerun',title,title_null,url)
                        continue

                    cnt_chk = 0
                    cnt_vol = item.find('td', 'date1').text.strip()
                    cnt_writer = str(item).split(';">')[1].split('</a')[0].strip()
                    cnt_price = item.find_all('td', 'date1')[1].find('strike').text.replace(",","").replace('\h','').split("P")[0].strip()
                    if item.find_all('td', 'date1')[1].find('font'):
                        cnt_price = item.find_all('td', 'date1')[1].find('font').text.replace(",","").split("P")[0].strip()

                    post_two  = s.get(url2)
                    soup = bs(post_two.text, 'html.parser')

                    cnt_fname = soup.find('span', 'font_layerlist').text.strip()
                    if cnt_fname == '/':
                        cnt_fname = soup.find_all('span', 'font_layerlist')[1].text.strip()

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
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("filerun 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filerun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
