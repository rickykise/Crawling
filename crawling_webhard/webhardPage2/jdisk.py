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

# ==================불법 업체==================

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://www.jdisk.com/board.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PHPSESSID=3te3kj5c1cslqjk3n5uc1p50k0; _bbsInfoTab=Y'
}

def startCrawling(site):
    with requests.Session() as s:
        i = 0;check = True
        link = 'http://www.jdisk.com/board.php?act=asyncList&banner_keyword=&searchKey=&searchValue=&search_keyword_hidden=&search_type='+site+'&search_keyword=&search=&useridx=&section='+site+'&sub_sec=&nPage='
        link2 = '&act=asyncList&mode=&s_act=&nLimit=20'
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i)+link2, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('table', id='contentList_Table').find_all('tr', 'dataRow')

            try:
                for item in tr:
                    adult = item.find('td', 'c_title').find('a')['onclick'].split("','")[1].split("','")[0]
                    if adult == '1':
                        continue
                    cnt_vol = item.find_all('td', 'c_data')[1].text.strip()
                    cnt_num = item.find('td', 'c_title').find('a')['onclick'].split("('")[1].split("','")[0]
                    url = "http://www.jdisk.com/board.php?act=bbs_info&idx="+cnt_num

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    title = soup.find('title').text.strip()
                    cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
                    cnt_writer = soup.find('table', 'file_detail').find_all('tr')[0].find_all('td', 'point_vol')[1].text.strip()
                    cnt_fname = soup.find('td', 'file_f').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'jdisk',
                        'Cnt_title': title,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': '0'
                    }
                    # print(data)

                    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("jdisk 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("jdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
