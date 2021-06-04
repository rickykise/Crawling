import requests,re
import pymysql,time,datetime
import urllib.parse
import pyautogui
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://m.sharebox.co.kr',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with requests.Session() as s:
        i = 0;a = 1;check = True

        while check:
            if i == 50:
                break
            Page = {
                'cate': site,
                'sort': 'New',
                'start': i,
                'subCate': '',
                'todo': 'mainContentsList'
            }
            link = 'http://m.sharebox.co.kr/index.php'
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('utf-8','replace'), 'html.parser')
            text = str(soup)
            i = i+10

            try:
                for item in text:
                    cnt_num = text.split('idx":"')[a].split('","')[0]
                    cnt_vol = text.split('filesize":"')[a].split('","')[0]
                    url = 'http://m.sharebox.co.kr/contents/index.php?idx='+cnt_num
                    a = a+1
                    if a == 11:
                        a = 1
                        break

                    post_two = s.get(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('utf-8','replace'), 'html.parser')
                    cnt_chk = 0

                    title = soup.find('li', 'viewn_title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('div', 'viewn_won').text.replace(",","").split('P')[0].strip()
                    cnt_writer = soup.find_all('span', 'pad_left5')[1].text.strip()
                    cnt_fname = soup.find('div', 'flist_titL').text.strip()
                    jehu = soup.find('li', 'btn_playinfoL').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'sharebox',
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

                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("sedisk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("sedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
