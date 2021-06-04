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

LOGIN_INFO = {
    'Frame_login': 'Ok',
    'idSave': '0',
    'm_id': 'up0001',
    'm_pwd': 'up0001',
    'x': '37',
    'y': '29'
}

def startCrawling(key):
    i = 0;check = True
    print('키워드 : '+key)

    with requests.Session() as s:
        login_req = s.post('https://fileman.co.kr/member/loginCheck.php', data=LOGIN_INFO)
        while check:
            i = i+1
            if i == 10:
                break
            print(str(i))
            try:
                encText = key.encode('euc-kr')
                encText = urllib.parse.quote(encText)
                link = 'http://fileman.co.kr/contents/?category1=&s_column=title&s_word='+encText+'&rows=20&show_type=0&sort=sort&page='+str(i)
                post_one  = s.get(link)
                c = post_one.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                table = soup.find('table', 'boardtype1')
                if soup.find('table', 'boardtype1') == None:
                    break
                tr = table.find('tbody').find_all('tr')

                for item in tr:
                    adult = item.find('td', 'title').find('a')['onclick'].split("', '")[2].split("'")[0]
                    if adult == '1':
                        continue
                    title = item.find('td', 'title').find('a')['title']
                    title_null = titleNull(title)
                    cnt_num = item.find('td', 'title').find('a')['onclick'].split("', '")[1].split("', '")[0]
                    url = 'http://fileman.co.kr/contents/view_top.html?idx='+cnt_num
                    url2 = 'http://fileman.co.kr/contents/view_top.html?idx='+cnt_num+'&amp;page='

                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    cnt_vol = item.find('td', 'size').text.strip()
                    cnt_writer = item.find('td', 'date').find('a').text.strip()


                    post_two  = s.get(url2)
                    content = post_two.content
                    soup2 = bs(content.decode('euc-kr','replace'), 'html.parser')
                    text = str(soup2)
                    tr = soup2.find('table', cellspacing='1').find_all('tr')[1]
                    cnt_chk = 0

                    cnt_price = tr.find_all('td')[6].text.strip().replace("\n","").replace("\t","").replace(" ","").split("P")[0]
                    cnt_fname = soup2.find('span', 'font_layerlist').text.strip()
                    if cnt_fname == "/":
                        cnt_fname = soup2.find_all('span', 'font_layerlist')[1].text.strip()
                    if text.find('저작권자와의 제휴') != -1:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileman',
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
                    # print('======================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("fileman 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("fileman 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
