import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
from urllib import parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    a = 0; check = True; insertNum = 0
    key = emoKey(key)
    print('키워드: ',key)
    try:
        enKey = urllib.parse.quote(key.encode('cp949'))
    except:
        print('특수문자')
        enKey = key.replace(' ', '')
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    while check:
        try:
            a = a+1
            print('페이지: ',a)
            if a == 100:
                break
            link = "http://greenbbs.clubbox.co.kr:8126/app/index.php?pageNo="
            link2 = "&c_no=&c_depth=1&listPerPage=&search_word="+enKey+"&search_col=b_subject&c_adult=N"
            r = requests.get(link+str(a)+link2)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find('div', 'file_list')
            tr = div.find('table').find_all('tr')
            if len(tr) < 4:
                break

            for item in tr:
                if item.find('td'):
                    td = item.find_all('td')
                    if len(td) == 7:
                        td = item.find_all('td')
                        if len(td) != 7:
                            continue
                        adult = item.find('a', id=re.compile("cutTitle_+"))['href'].split("', '")[1].split("'")[0]
                        if adult == '1':
                            continue
                        cnt_fname = item.find('ul').find('li').text.strip()
                        cnt_vol = item.find('td', 'file_cash_info').text.strip()
                        cnt_num = item.find('a', id=re.compile("cutTitle_+"))['id'].split("cutTitle_")[1]
                        url = 'http://greenbbs.clubbox.co.kr:8126/app/index.php?b_no='+cnt_num+'&control=view'

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        table = soup.find('div', 'scroll_file_down').find('table')
                        cnt_price = 0;returnValue = []

                        title = soup.find('a', 'b_twitter')['href'].split("', '")[1].split("'")[0]
                        title_null = titleNull(title)
                        # 키워드 체크
                        getKey = getKeyword(conn,curs)
                        keyCheck = checkTitle(title_null, getKey)
                        if keyCheck['m'] == None:
                            continue
                        keyCheck2 = checkTitle2(title_null, getKey)
                        if keyCheck2['m'] == None:
                            continue
                        tr = table.find_all('tr')
                        for item in tr:
                            cnt_price = int(item.find_all('td')[3].text.replace(",", "").strip().split("C")[0])
                            returnValue.append(cnt_price)
                        for i in range(len(tr)-1):
                            cnt_price = returnValue[i]+cnt_price

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'clubbox',
                            'Cnt_title': title,
                            'Cnt_title_null': title_null,
                            'Cnt_url': url,
                            'Cnt_price': cnt_price,
                            'Cnt_writer' : '',
                            'Cnt_vol' : cnt_vol,
                            'Cnt_fname' : cnt_fname,
                            'Cnt_chk': '1'
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
                        continue
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

    print("clubbox 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("clubbox 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
