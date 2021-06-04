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

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://www.filesun.com/disk/board.php',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': 'SUNSSID=8lomvljtai452csag0ckhi2oh3; _ga=GA1.2.408650097.1547184976; _gid=GA1.2.31476081.1547184976; _gat=1; exceptadult=1'
        }
        link = "http://www.filesun.com/disk/board.php?board="+site+"&exceptadult=1&page="
        while check:
            i = i+1
            if i == 4:
                break
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            table = soup.find('table', 'listTable').find('tbody')
            tr = table.find_all('tr', 'colorBlock1')
            # try:
            for item in tr:
                cnt_num = item.find_all('td')[1]['class'][1]
                href = item.find('a')['href']
                url = 'http://www.filesun.com' + href
                cnt_vol = item.find('td', 'size').text.strip()
                cnt_price = item.find('td', 'downpoint').text.strip().replace(" ","").replace(",","").split("→ ")[1].split("P")[0]

                post_two  = s.get(url)
                soup2 = bs(post_two.text, 'html.parser')

                title = soup2.find('title').text.strip().split(" 다운로드")[0]
                title_null = titleNull(title)
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    dbResult = insertDB('filesun',title,title_null,url)
                    continue
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    dbResult = insertDB('filesun',title,title_null,url)
                    continue
                print('===============================================')
                # checkPrice = str(keyCheck['p'])
                # if checkPrice == cnt_price:
                #     cnt_chk = 1
                cnt_writer = soup2.find('td', colspan='2').text.strip().replace(" ","")
                cnt_fname = soup2.find('div', 'file').text.strip().replace(" ","")

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filesun',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_chk': '0'
                }
                # print(data)

                # dbResult = insertALL(data)
            # except:
            #     continue

if __name__=='__main__':
    start_time = time.time()

    print("filesun 크롤링 시작")
    site = ['1&listmode=all','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("filesun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
