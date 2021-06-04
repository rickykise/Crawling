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
    'keep': 'N',
    'm_id': 'dlsrlwkr@naver.com',
    'm_pwd': 'dlsrl11!',
    'view_login': 'N'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    while check:
        with requests.Session() as s:
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Length': '110',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'smartfile.co.kr',
                'Referer': 'http://smartfile.co.kr/contents/?category1='+site+'&limit=',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }

            login_req = s.post('http://ssl.smartfile.co.kr/member/loginCheck.php', data=LOGIN_INFO)
            post_one  = s.get('http://smartfile.co.kr/charge/')
            soup = bs(post_one.text, 'html.parser')

            Page = {
                'category1': site,
                'category2': '',
                'chkcopy': '',
                'limit': '0',
                'opr': 'true',
                'page': i,
                'page_su': '10',
                's_word': '',
                'sort1': '',
                'sort2': '',
                'type': 'json',
                'uploader': ''
            }
            i = i+1
            if i == 4:
                break
            post_one  = s.post("http://smartfile.co.kr/contents/contents_list_inc.php", data=Page, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)

            # try:
            for item in text:
                if a == 25:
                    a = 1
                    break
                cnt_num = text.split('"id":"')[a].split('","')[0]
                adult = text.split('"flag_adult":"')[a].split('","')[0]
                a = a+1
                url = 'http://smartfile.co.kr/contents/view.php?gg=1&idx='+cnt_num
                if adult == '1':
                    continue

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

                # 키워드 체크
                # getKey = getKeyword()
                # keyCheck = checkTitle(title_null, getKey)
                # if keyCheck['m'] == None:
                #     dbResult = insertDB('smartfile',title,title_null,url)
                #     continue
                # keyCheck2 = checkTitle2(title_null, getKey)
                # if keyCheck2['m'] == None:
                #     dbResult = insertDB('smartfile',title,title_null,url)
                #     continue

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
                print(data)
                print('============================================')

                    # dbResult = insertALL(data)
            # except:
            #     continue

    time.sleep(90)

if __name__=='__main__':
    start_time = time.time()

    print("smartfile 크롤링 시작")
    site = ['DRA','MED','MVO','ANI']
    for s in site:
        startCrawling(s)
    print("smartfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
