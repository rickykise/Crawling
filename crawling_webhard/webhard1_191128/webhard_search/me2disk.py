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

def startCrawling(key):
    i = 0;check = True
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        link = "http://me2disk.com/contents/search.php?category1=&s_column=title&sCode="+encText+"&emCopy=N&adultEx=Y&s_word="+encText+"#"
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            table = soup.find_all('table', 'boardtype1')[1].find('tbody')
            tr = table.find_all('tr', 'bbs_list')
            try:
                for item in tr:
                    cnt_num = item['data-idx']
                    url = 'http://me2disk.com/contents/view.htm?idx='+cnt_num+'&viewPageNum='
                    post_two  = s.get(url)
                    soup = bs(post_two.text, 'html.parser')
                    view = soup.find('table', 'view_tb')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('me2disk',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('me2disk',title,title_null,url)
                    #     continue
                    cnt_price = view.find_all('td')[1].text.strip().replace(",","").split("P")[0]
                    cnt_writer = soup.find('span', 'bold mar_rig5').text.strip()
                    cnt_vol = view.find_all('td')[3].text.strip()
                    cnt_fname = soup.find('div', 'view_name3').text.strip()
                    if soup.find('li', 'tit_le2'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'me2disk',
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

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("me2disk 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("me2disk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
