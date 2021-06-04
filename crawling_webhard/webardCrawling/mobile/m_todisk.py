import requests,re
import pymysql,time,datetime
import urllib.parse
import base64
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Origin': 'http://m.todisk.com',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Cookie': 'appLogin=false; PHPSESSID=4513ea4563f87af45d1c741c755bb76a; log100=20190122; _ga=GA1.2.1070817977.1548124083; _gid=GA1.2.1882185260.1548124083; think_result=0; shacipher=Y; is_ctrl=Y; m_grade=1; mid=AvW14mtZM1qL1fJ2GITOhXQIdHDBrOCK2ZrmYSdgK2IKuZfVzCFenSbMnejn7xoCEB4DHWrPRmlFJLgNW1yQ1xMDSIffZSWpPXCkipajc3QUFkXX36T0TvaKcWc519lM; nick=up0001; Usr=up0001; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; LogChk=Y; _not100=Y; cidprt=Y; logtime=1548124086; logip=1028813252; vr=1'}

LOGIN_INFO = {
    'act': 'ok',
    'mb_id': 'up0001',
    'mb_id1': 'up0001',
    'mb_pw': 'up0001',
    'pwd_save': 'N',
    'repage': '/mobile/storage.php',
    'securityLogin': '1'
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('https://ssl.todisk.com/login_step_m_new.php', data=LOGIN_INFO, headers=headers)
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'Limit': '20',
                'ListMode': 'list',
                'Page': i,
                'Search': '',
                'SearchKey': '',
                'Search_radio': '',
                'Search_re': '',
                'Search_sort': '',
                'act': 'load_list_page',
                'click': '',
                'is_search_str': '',
                'mSec': site,
                'onlyTitle': '',
                'sSec': 'all',
                'subsearch': ''
            }
            link = 'http://m.todisk.com/mobile/storage.php'
            post_one  = s.post(link, headers=headers, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', 'list_board_list3')

            try:
                for item in div:
                    adult = item['onclick'].split("','")[1].split("','")[0]
                    if adult == '1':
                        continue
                    cnt_num = item['onclick'].split("('")[1].split("','")[0]
                    baseCnt = str(base64.b64encode(cnt_num.encode('utf-8'))).split("'")[1].split("'")[0]
                    url = 'http://m.todisk.com/mobile/storage.php?act=view&idx='+cnt_num+'&eidx='+baseCnt
                    url2 = 'http://www.todisk.com/_main/popup.php?doc=bbsInfo&idx='+cnt_num+'&eidx='+baseCnt

                    post_two  = s.post(url2, headers=headers)
                    soup = bs(post_two.text, 'html.parser')

                    table = soup.find('table', 'table2')
                    table2 = soup.find_all('table', 'table2')[1]
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split("투디스크 -")[1].split("상세정보")[0]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = table2.find('td').text.strip().replace(" ", "").replace(",", "").split("P")[0]
                    cnt_writer = table2.find_all('td')[1].text.strip()
                    cnt_fname = table.find('td')['title']
                    if table.find_all('td')[1].find('img'):
                        cnt_fname = soup.find('table', 'table3_in').find('th')['title']
                    if table2.find('td').find('img'):
                        cnt_chk = 1

                    post_three  = s.post(url, headers=headers)
                    soup = bs(post_three.text, 'html.parser')
                    cnt_vol = soup.find('div', 'play_list_title_name').text.split("|")[2].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'todisk',
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

    print("m_todisk 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_todisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
