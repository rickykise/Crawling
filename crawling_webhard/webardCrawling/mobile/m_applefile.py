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
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;a = 1;check = True
    link = 'https://m.applefile.com/module/contents/list.php'
    while check:
        if i == 4:
            break
        Page = {
            'limit': '20',
            'pn': i,
            'tab': site
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'PHPSESSID=uevc7miq8usrc2k9pcaocicuns; seller=; seller_contents=%7B%22type%22%3A%22tab5%22%2C%22name%22%3A%22contents_tab5%22%2C%22cate1%22%3A%22%22%2C%22idx%22%3A%2230000729%22%7D; right_tab=1; right_tab1=%7B%22type%22%3A%22tab1%22%2C%22name%22%3A%22contents_tab1%22%2C%22idx%22%3A%2230000729%22%7D',
            'Host': 'm.applefile.com',
            'Referer': 'https://m.applefile.com/contents/',
            'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        i = i+1

        r = requests.post(link, data=Page, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup).split('</a>')[0].strip()
        json_obj = json.loads(text)

        try:
            for item in json_obj['list']:
                title = item['title']
                title_null = titleNull(title)
                cnt_num = item['idx']
                url = 'https://m.applefile.com/contents/#tab='+site+'&idx='+str(cnt_num)
                cnt_price = str(item['cash']).replace(",","")
                cnt_writer = item['nickname']

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                ajax_url = 'https://m.applefile.com/module/contents/view.php'
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
                cnt_vol = json_obj['all_size']
                for item in json_obj['file']:
                    cnt_fname = item['file_name']

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
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'applefile',
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
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("m_applefile 크롤링 시작")
    site = ['DRA','MED','ANI','MVO']
    for s in site:
        startCrawling(s)
    print("m_applefile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
