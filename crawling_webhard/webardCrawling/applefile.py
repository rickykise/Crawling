import requests,re
import pymysql,time,datetime
import urllib.parse
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.applefile.com/module/contents/list.php'
    while check:
        if i == 5:
            break
        data = {
            'pn': i,
            'tab': site
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'PHPSESSID=uevc7miq8usrc2k9pcaocicuns',
            'Host': 'www.applefile.com',
            'Referer': 'https://www.applefile.com/contents/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'X-Requested-With': 'XMLHttpRequest'
        }
        i = i+1
        r = requests.post(link, data=data, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup).split('</a>')[0].strip()
        json_obj = json.loads(text)

        try:
            for item in json_obj['list']:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                title = item['title']
                title_null = titleNull(title)
                cnt_num = item['idx']
                url = 'https://www.applefile.com/contents/view.html?idx='+cnt_num
                cnt_vol = item['size']
                cnt_price = str(item['cash']).replace(",","")
                cnt_writer = item['nickname']

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('applefile',title,title_null,url)
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('applefile',title,title_null,url)
                    continue

                ajax_url = 'https://www.applefile.com/module/contents/view.php'
                cnt_chk = 0
                data2 = {
                    'idx': cnt_num,
                    'type': 'file'
                }

                r = requests.post(ajax_url, data=data2, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup).split('</a>')[0].strip()
                json_obj = json.loads(text)

                for item in json_obj['file']:
                    cnt_fname = item['realname']

                data3 = {
                    'idx': cnt_num,
                    'type': 'info'
                }
                r = requests.post(ajax_url, data=data3)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup).split('</p>')[0].strip()
                json_obj = json.loads(text)

                jehu = json_obj['chkcopy']
                if jehu == 'Y':
                    cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num, #게시물 번호
                    'Cnt_osp' : 'applefile', #사이트
                    'Cnt_title': title, #제목
                    'Cnt_title_null': title_null,
                    'Cnt_url': url, #url
                    'Cnt_price': cnt_price, #가격
                    'Cnt_writer' : cnt_writer, #작성
                    'Cnt_vol' : cnt_vol, #용량
                    'Cnt_fname' : cnt_fname, #파일명
                    'Cnt_regdate' : now, #등록일
                    'Cnt_chk': cnt_chk
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("applefile 크롤링 시작")
    site = ['DRA','MED','ANI','MVO']
    for s in site:
        startCrawling(s)
    print("applefile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
