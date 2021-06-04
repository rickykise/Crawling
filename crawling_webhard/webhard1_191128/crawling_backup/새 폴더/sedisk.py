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
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://sedisk.com/storage.php',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'ACEFCID=UID-5C22F965D514161EE9381054; _ga=GA1.2.1287727625.1545974475; ptn=ksc0110; ACEUCI=1; _gid=GA1.2.1421021257.1547447786; evLayer=N; _gat=1'
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with requests.Session() as s:
        i = 0;check = True
        link = 'http://sedisk.com/storage.php?act=asyncList&banner_keyword=&searchKey=&searchValue=&search_keyword_hidden=&search_type='+site+'&search_keyword=&search=&useridx=&section='+site+'&sub_sec=&nPage='
        link2 = '&act=asyncList&mode=&s_act=&media_idx=&nLimit=20'
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
                    cnt_num = item.find('td', 'c_title').find('a')['onclick'].split("('")[1].split("','")[0]
                    url = 'http://sedisk.com/storage.php?act=view&idx=' + cnt_num

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('span', 'b_price').text.strip().split("P")[0].replace(",","")
                    cnt_vol = soup.find('span', 'f_tahoma11').text.strip().replace("/ ","")
                    cnt_writer = soup.find('span', 'name_s').text.strip()
                    cnt_fname = soup.find('td', 'td_tit').text.strip()
                    if soup.find_all('td', 'point_vol')[2].find('img'):
                        img = soup.find_all('td', 'point_vol')[2].find('img')['src']
                        if img.find('ico_jehu2') != -1:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'sedisk',
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

                    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        # pass
                    finally :
                        conn.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("sedisk 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("sedisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
