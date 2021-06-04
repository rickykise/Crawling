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
    i = 0;a = 1;check = True
    print(key)
    encText = key.encode('euc-kr')
    encText = urllib.parse.quote(encText)
    LOGIN_INFO = {
        'Frame_login': 'Ok',
        'keep': 'Y',
        'm_id': 'b9xhatv2XXG5ufWAuCTu9LDEEfG/k1kLUyyvGjUoloY=||S4G0JRkd762d09dd02366f8d1b132108f4837d5',
        'm_pwd': 'UytaRRPgYWgen9WuabRaww==||s9f4dy7040b0749bfb2243fea198606a2534df6',
        'view_login': 'N'
    }
    with requests.Session() as s:
        login_req = s.post('https://ssl.smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO)
        post_one  = s.get('http://smartfile.co.kr/charge/')
        soup = bs(post_one.text, 'html.parser')
        while check:
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Host': 'smartfile.co.kr',
                'Referer': 'http://smartfile.co.kr/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }

            Page = {
                'category1': '',
                's_column': 'all',
                's_word': encText
            }
            i = i+1
            if i == 4:
                break
            post_one  = s.get("http://smartfile.co.kr/contents/search.php?category1=&s_column=all&s_word="+encText, data=Page, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find_all('tr', id=re.compile("row_+"))

            try:
                for item in tr:
                    cnt_num = item['id'].split('row_')[1]
                    url = 'http://smartfile.co.kr/contents/view.php?gg=1&idx='+cnt_num

                    headers2 = {
                            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'ko-KR',
                            'Connection': 'Keep-Alive',
                            'Host': 'smartfile.co.kr',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                    }
                    r = s.get(url, headers=headers2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    table = soup.find('table', summary='컨텐츠정보표').find('tbody')
                    cnt_chk = 0

                    title = soup.find('title').text.strip()
                    title_null = titleNull(title)

                    cnt_price = table.find_all('td')[2].find('span').text.strip().split("P")[0].replace(",","")
                    cnt_vol = table.find_all('td')[2].text.strip().replace(" ","").split("/")[0]
                    cnt_writer = table.find_all('td')[3]['onclick'].split("', '")[1].split("', '")[0]
                    cnt_fname = soup.find('span', 'file_name').text.strip()
                    if table.find_all('td')[2].find('img'):
                        jehu = table.find_all('td')[2].find('img')['title']
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'smartfile',
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
                    # print('============================================')

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("smartfile 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
