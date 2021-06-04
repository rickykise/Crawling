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
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'Limit': '20',
                'Page': i,
                'Search': '',
                'SearchKey': '',
                'is_mobile': '',
                'mCate': site,
                'relate': '',
                'sCate': 'all'
            }
            link = 'http://m.mfile.co.kr/storage.php?act=load_list_page'

            post_one  = s.post(link, headers=headers, data=Page)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find_all('li')
            try:
                for item in li:
                    cnt_num = item['onclick'].split("load_view('")[1].split("')")[0]
                    url = 'http://m.mfile.co.kr/index.php?act=view&idx=' + cnt_num
                    url2 = 'http://www.mfile.co.kr/storage.php?act=view&idx='+cnt_num+'&search_sort=undefined'

                    r = requests.get(url2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split("- ")[1]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('span', id='chkPacket').text.replace(",","").strip()
                    cnt_writer = soup.find('font', 'name_s').text.strip()
                    cnt_vol = soup.find('span', id='chkSize').text.replace(",","").strip()
                    cnt_fname = soup.find('td', 'td_tit').text.strip()

                    if soup.find('td', 'td_tit').find('img'):
                        aaa = soup.find('td', 'td_tit').find('img')['src']
                        if aaa.find('icon_alli') != -1:
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'mfile',
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

    print("m_fileguri 크롤링 시작")
    site = ['','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_fileguri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
