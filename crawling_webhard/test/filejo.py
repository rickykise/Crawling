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

def startCrawling():
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        link = 'http://www.filejo.com'
        post_cookie  = s.get(link)
        cntCookie = str(s.cookies).split('cntCookie=')[1].split(' ')[0]

        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Cookie': 'log_id=undersd01; sellinfo=0; cntCookie='+cntCookie,
            'Host': 'ssl.filejo.com',
            'Referer': 'http://www.filejo.com/main/main_html.php',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)'
        }

        link2 = 'https://ssl.filejo.com/main/module/loginPrc_auth.php?callback=jQuery16405734686777607637_1552537000973&act=ok&mb_id=undersd01&mb_pw=undersd8556&log_save=Y&cpChk=Y'
        login_req = s.post(link2, headers=headers)
        cookie = login_req.headers.get('Set-Cookie')
        phpsessid = cookie.split('PHPSESSID=')[1].split(';')[0]
        cntCookie = cookie.split('cntCookie=')[1].split(';')[0]

        headers2 = {
            'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Cookie': 'log_id=undersd01; cntCookie='+cntCookie+'; loginDiv=1; mid=0a191a199719e619f61987199719j619c619; AutoPayING=N; grade=1; credit=0%7C%7C0; sellinfo=0; reTurner=F; adult=1; broadCnt=0; coupon=0; mypageCnt=0%7C%7C0%7C%7C0%7C%7C0%7C%7CN%7C%7C0%7C%7C0%7C%7C0%7C%7CN; LogChk=Y; sex=2; PHPSESSID='+phpsessid+'; memo_cnt=4',
            'Host': 'www.filejo.com',
            'Referer': 'http://www.filejo.com/',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)'
        }
        post_one  = s.get('http://www.filejo.com/main/storage.php?section=', headers=headers2)
        # soup = bs(post_one.text, 'html.parser')
        # print(soup)

        data = {
            'code_cate=': 'MOV',
            'code_title': 'aaa'
        }
        # link = 'http://upimg.filejo.com/main/module/uploadPrc.php'
        link = 'http://upimg.filejo.com/main/editor/upload_new.php?code_cate=&code='
        post_one  = s.get(link)
        soup = bs(post_one.text, 'html.parser')
        print(soup)


        # 'title': '가면라이더 빌드-03화',
        # 'filepath': 'c:\\Users\\user\Desktop\가면라이더빌드\가면라이더 빌드-03화\가면라이더 빌드_03화.mkv',
        # 'code_cate': 'ANI',
        # 'code': 'ANI_008',
        # 'code_title': 'ANI',
        # 'option_title': 'sdfsd',
        # 'filename': '가면라이더 빌드_02화'
        # link = 'http://www.filejo.com/main/main_html.php'
        # post_one  = s.get(link, cookies=cookies)
        # soup = bs(post_one.text, 'html.parser')
        # print(soup)



        # 'title': '가면라이더 빌드-03화',
        # 'filepath': 'C:\Users\user\Desktop\가면라이더빌드\가면라이더 빌드-03화\가면라이더 빌드_03화.mkv',
        # 'code_cate': 'ANI',
        # 'code': 'ANI_008',
        # 'code_title': 'ANI',
        # 'option_title': 'sdfsd',
        # 'filename': '가면라이더 빌드_02화',
        # 'filetype': 'MKV',
        # 'mmsv_files': 'asd',
        # 'uploader': 'asd',
        # 'passMP3': 'N',
        # 'agreeEncode': 'sad'



if __name__=='__main__':
    start_time = time.time()

    print("filejo 크롤링 시작")
    startCrawling()
    print("filejo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
