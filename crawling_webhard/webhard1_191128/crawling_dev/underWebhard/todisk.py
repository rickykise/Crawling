import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
import base64
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {'Cookie': 'appLogin=false; PHPSESSID=4513ea4563f87af45d1c741c755bb76a; log100=20190122; _ga=GA1.2.1070817977.1548124083; _gid=GA1.2.1882185260.1548124083; think_result=0; shacipher=Y; is_ctrl=Y; m_grade=1; mid=AvW14mtZM1qL1fJ2GITOhXQIdHDBrOCK2ZrmYSdgK2IKuZfVzCFenSbMnejn7xoCEB4DHWrPRmlFJLgNW1yQ1xMDSIffZSWpPXCkipajc3QUFkXX36T0TvaKcWc519lM; nick=up0001; Usr=up0001; total_cash=0; cmn_cash=0; bns_cash=0; coupon=0; memo_cnt=0; LogChk=Y; _not100=Y; cidprt=Y; logtime=1548124086; logip=1028813252; vr=1'}

def startCrawling(key):
    i = 0; a = 1;check = True;insertNum = 0
    key = emoKey(key)
    print('키워드: ',key)
    try:
        enKey = urllib.parse.quote(key.encode('cp949'))
    except:
        print('특수문자')
        enKey = key.replace(' ', '')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with requests.Session() as s:
        post_one  = s.post('http://www.todisk.com/_main/', headers=headers)
        while check:
            try:
                i = i+1
                print(i)
                if i == 100:
                    break
                link = 'http://www.todisk.com/_main/storage.php?s_act2=ok&search_type=all&search_keyword=total_search&search='+enKey+'&p='
                post_one  = s.post(link+str(i), headers=headers)
                soup = bs(post_one.text, 'html.parser')
                if soup.find('div', id='list_sort'):
                    div = soup.find('div', id='list_sort')
                    tr = div.find('table').find_all('tr')

                    for item in tr:
                        adult = item.find_all('td')[1]['onclick'].split("','")[1].split("'")[0]
                        if adult == '1':
                            continue
                        cnt_num = item.find('input')['value']
                        baseCnt = str(base64.b64encode(cnt_num.encode('utf-8'))).split("'")[1].split("'")[0]
                        url = 'http://www.todisk.com/_main/popup.php?doc=bbsInfo&idx='+cnt_num+'&eidx='+baseCnt

                        post_two  = s.post(url, headers=headers)
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
                        cnt_vol = table2.find('td').text.strip().replace(" ", "").split("/")[1]
                        cnt_fname = table.find('td')['title']
                        if table.find_all('td')[1].find('img'):
                            cnt_fname = soup.find('table', 'table3_in').find('th').text.strip()
                        if table2.find('td').find('img'):
                            cnt_chk = 1

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
                            if dbResult == True:
                                continue
                            else:
                                insertNum = insertNum+1
                        finally :
                            conn2.close()
                else:
                    break
            except:
                continue

        print("insert : ",insertNum)
        print('==================================================================')

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getUnderSearchKey(conn,curs)
    conn.close()

    print("todisk 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("todisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
