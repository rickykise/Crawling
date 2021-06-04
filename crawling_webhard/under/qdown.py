import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    print('키워드: ',key)
    key = emoKey(key)
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True;insertNum = 0
    with requests.Session() as s:
        while check:
            try:
                i = i+1
                print(i)
                if i == 100:
                    break
                link = 'http://www.qdown.com/main/doc/storage_/list_ajax_.php?ver=20180202&sale=&mainB=&mainA=&?t=1548060516592&section=&list_count=20&p='+str(i)+'&search='+key
                print(link)
                post_one  = s.get(link)
                soup = bs(post_one.text, 'html.parser')
                idx = soup.find_all('td', 'black_a_s')
                if len(idx) < 2:
                    break

                for item in idx:
                    adult = item.find('a')['onclick'].split("','")[1].split("','")[0]
                    if adult == '1':
                        continue
                    cnt_num = item.find('a')['onclick'].split("winBbsInfo('")[1].split("','")[0]
                    url = 'http://www.qdown.com/main/popup/bbs_info.php?idx='+cnt_num

                    post_two  = s.get(url)
                    c = post_two.content
                    soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                    text = str(soup)
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
                    cnt_price = soup.find('td', 'infotable_td2').text.replace(" ","").replace(",","").split("P")[0].strip()
                    cnt_vol = soup.find('td', 'infotable_td2').text.replace(" ","").split("/")[1].strip()
                    cnt_writer = text.split("target_nick=")[1].split('","')[0]
                    cnt_fname = soup.find('td', 'infotable_list_td1').text.strip()
                    if soup.find('td', 'infotable_td2').find('img'):
                        jehu = soup.find('td', 'infotable_td2').find('img')['title']
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'qdown',
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

    print("qdown 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("qdown 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
