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
    'Accept': 'text/html, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://www.dodofile.com/board',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'opVal=1%7C1%7C0%7C1%7C0%7C0%7C0%7C0; PHPSESSID=49et3iqga9tssikfn4ggofme20; ACEFCID=UID-5C511801779491C04E7D2707; ACEUCI=1; _bbsInfoTab=Y; mi^c=2019-01-30%2012%3A20%3A37; mi^vi=JI0XN1IDQ1z7JKIQM2IEX125'
    }

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;insertNum = 0;check = True
    print(site)
    with requests.Session() as s:
        while check:
            try:
                i = i+1
                link = 'http://www.dodofile.com/board.php?act=asyncList&search_type=ALL&section='+site+'&nPage='+str(i)+'&act=asyncList&mode=&s_act=&nLimit=100&_=1548819953871'
                print('페이지: ', str(i))
                post_one  = s.get(link, headers=headers)
                soup = bs(post_one.text, 'html.parser')
                table = soup.find('table', id='contentList_Table')
                tr = table.find_all('tr', 'dataRow')
                if len(tr) < 90:
                    print('게시물 없음')
                    check=False;break

                for item in tr:
                    cnt_num = item['data-idx']
                    url = 'http://www.dodofile.com/board.php?act=bbs_info&idx='+cnt_num

                    post_two  = s.get(url)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
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
                    cnt_price = soup.find('span', 'b_price').text.strip().replace(",","").replace(" ","").split("P")[0]
                    cnt_writer = soup.find_all('td', 'point_vol')[1].text.strip()
                    cnt_vol = soup.find('span', 'f_tahoma11').text.replace(" ","").strip().split(":")[1].split("/")[0]
                    cnt_fname = soup.find('li', 'file_f').text.strip()
                    # cnt_chk

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'dodofile',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': 0
                    }
                    # print(data)

                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                        if dbResult == True:
                            continue
                        else:
                            insertNum = insertNum+1
                    finally :
                        conn2.close()
            except:
                continue
            print("insert : ",insertNum)
            print('==================================================================')


if __name__=='__main__':
    start_time = time.time()

    print("dodofile 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    # site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("dodofile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
