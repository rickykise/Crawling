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

def startCrawling(key):
    print(key)
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            print('페이지: ',i)
            if i == 50:
                break
            link = 'http://www.dodofile.com/board.php?act=asyncList&search_type=ALL&section=ALL&nPage='+str(i)+'&search_keyword=&search='+key+'&act=asyncList&mode=&s_act=&nLimit=20&_=1548819953871'
            try:
                post_one  = s.get(link, headers=headers)
                soup = bs(post_one.text, 'html.parser')
                table = soup.find('table', id='contentList_Table')
                tr = table.find_all('tr', 'dataRow')
                if len(tr) < 2:
                    print('게시물없음')
                    break

                for item in tr:
                    cnt_num = item['data-idx']
                    url = 'http://www.dodofile.com/board.php?act=bbs_info&idx='+cnt_num

                    post_two  = s.get(url)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    cnt_price = soup.find('span', 'b_price').text.strip().replace(",","").replace(" ","").split("P")[0]
                    cnt_writer = soup.find_all('td')[1].text.strip()
                    cnt_vol = soup.find('span', 'f_tahoma11').text.replace(" ","").strip().split("/")[0]
                    cnt_fname = soup.find('li', 'file_f').text.strip()
                    if soup.find('span', 'pl10').find('img'):
                        jehu = soup.find('span', 'pl10').find('img')['src']
                        if jehu.find('jehu.gif') != -1:
                            cnt_chk = 1

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
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print('=====================================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("dodofile 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("dodofile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
