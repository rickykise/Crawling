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

LOGIN_INFO = {
    'Frame_login': 'Ok',
    'idSave': '0',
    'm_id': 'up0001',
    'm_pwd': 'up0001',
    'm_pwd_load': '',
    'm_pwd_pass': '',
    'x': '27',
    'y': '29'
}

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0; a = 1;check = True
    # print(site)
    with requests.Session() as s:
        login_req = s.post('https://g-disk.co.kr/member/loginCheck2.php', data=LOGIN_INFO)
        while check:
            i = i+1
            # print('페이지: ',i)
            if i == 4:
                break
            link = 'http://g-disk.co.kr/contents/?category1='+site+'&category2=&s_column=&s_word=&rows=50&sort=&show_type=0&page='
            post_one  = s.post(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            tbody = soup.find('table', 'boardtype2').find('tbody')
            tr = tbody.find_all('tr', 'reply')
            try:
                for item in tr:
                    adult = item.find('a')['onclick'].split("', '")[2].split("')")[0]
                    if adult == '1':
                        continue
                    cnt_writer = item.find_all('td', 'date')[1].text.strip()

                    cnt_price = item.find_all('td', 'date1')[1].text.strip().replace(" ","").replace(",","").strip().split('P')[0]
                    cnt_vol = item.find_all('td', 'date1')[0].text.strip()

                    cnt_num = item.find('td', 'num').text.strip()
                    url = 'http://g-disk.co.kr/contents/view.htm?idx='+cnt_num
                    url2 = 'http://g-disk.co.kr/contents/view_top.html?idx='+cnt_num
                    r = requests.get(url2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)
                    table = soup.find_all('table', height='34')[1]
                    table2 = soup.find_all('table', cellpadding='0')[10]
                    cnt_chk = 0

                    title = table.find('span').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('gdisk',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('gdisk',title,title_null,url)
                        continue
                    cnt_fname = soup.find_all('span', 'font_layerlist')[1].text.strip()
                    if text.find('저작권자와의 제휴를') != -1:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'gdisk',
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
                        insertDB('gdisk',title,title_null,url)
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("gdisk 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("gdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
