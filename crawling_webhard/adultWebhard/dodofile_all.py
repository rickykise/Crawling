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
    print(key)
    i = 0;check = True
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://www.dodofile.com/board',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    with requests.Session() as s:
        post_one  = s.get('http://www.dodofile.com', headers=headers)
        soup = bs(post_one.text, 'html.parser')
        div = soup.find('div', id='contentsLeft')
        adtme = div.find_all('input')[1]['value']
        parrot = div.find_all('input')[6]['value']

        LOGIN_INFO = {
            'adtme': adtme,
            'httpsurl': 'https://guard.dodofile.com/models/common/main/login/loginPrc_ssl.php',
            'httpurl': '/models/common/main/login/loginPrc_ssl.php',
            'mb_id': 'up003',
            'mb_pw': 'up003',
            'parrot': parrot,
            'renew': 'ok',
            'sSiteNameLogin': 'dodofile.com',
            'secure': 'Y'
        }

        login_req = s.post('https://guard.dodofile.com/models/common/main/login/loginPrc_ssl.php', data=LOGIN_INFO, headers=headers)
        logsoup = bs(login_req.text, 'html.parser')
        headers = login_req.headers
        text = str(headers)
        sUserPay = text.split(', sUserPay=')[1].split(';')[0]
        sUserInfo = text.split(', sUserInfo=')[1].split(';')[0]

        headers2 = {
            'Accept': 'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'http://www.dodofile.com/board',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'sUserPay='+sUserPay+'; paycnt=0; sUserInfo='+sUserInfo+'; adult=1; cmn_cash=0; sell_cash=0; bns_cash=500; d_coupon=0; mile_cash=0; memo_cnt=0; nameauth=Y; nkinoid=up003; nCompanyIdx=2'
        }
        while check:
            i = i+1
            print('페이지: ',i)
            if i == 50:
                break
            link = 'http://www.dodofile.com/board.php?act=asyncList&search_type=ALL&section=ALL&nPage='+str(i)+'&search_keyword=&search='+key+'&act=asyncList&mode=&s_act=&nLimit=20&_=1548819953871'
            post_two  = s.get(link, headers=headers2)
            soup2 = bs(post_two.text, 'html.parser')
            table = soup2.find('table', id='contentList_Table')
            tr = table.find_all('tr', 'dataRow')
            if len(tr) < 2:
                print('게시물없음')
                break
            try:
                for item in tr:
                    cnt_num = item['data-idx']
                    url = 'http://www.dodofile.com/board.php?act=bbs_info&idx='+cnt_num

                    post_two  = s.get(url, headers=headers2)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = jayeGetKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('dodofile',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('dodofile',title,title_null,url)
                        continue
                    cnt_price = soup.find('span', 'b_price').text.strip().replace(",","").replace(" ","").split("P")[0]
                    cnt_writer = soup.find_all('td', 'point_vol')[1].text.strip()
                    cnt_vol = soup.find('span', 'f_tahoma11').text.replace(" ","").strip().split(":")[1].split("/")[0]
                    cnt_fname = soup.find('li', 'file_f').text.strip()

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
                    # print('=====================================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("dodofile 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("dodofile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
