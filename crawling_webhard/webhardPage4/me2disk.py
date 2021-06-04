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
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        link = "http://me2disk.com/contents/index.htm?category1="+site+"&adultEx=Y#"
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
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('me2disk',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('me2disk',title,title_null,url)
                        continue
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
                        insertDB('me2disk',title,title_null,url)
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue


if __name__=='__main__':
    start_time = time.time()

    print("me2disk 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("me2disk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
