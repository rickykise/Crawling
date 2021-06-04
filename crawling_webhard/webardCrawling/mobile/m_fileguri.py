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
    i = 0;a = 2;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = "https://m.fileguri.com/api/content/list.php?cate="+site+"&search_type=title&is_rights=y&adult_not=y&page="+str(i)
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Length': '0',
                'Host': 'm.fileguri.com',
                'Referer': 'https://m.fileguri.com/?cate='+site+'&search_type=title&is_rights=y&adult_not=y&page='+str(i),
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                'X-Requested-With': 'XMLHttpRequest'
            }
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    if a == 77:
                        a = 2
                        break
                    cnt_num = text.split('link":"')[a].split('","')[0].split('idx=')[1]
                    url = 'https://m.fileguri.com/api/content/view.php?idx='+cnt_num
                    a = a+1

                    post_two  = s.get(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    textJ = str(soup)
                    jsonString = json.loads(textJ)
                    cnt_chk = 0

                    textJson = str(jsonString)
                    title = textJson.split("'title': '")[1].split("',")[0].strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = textJson.split("'sale_point': '")[1].split("',")[0].replace(",","")
                    cnt_writer = textJson.split("'up_nickname': '")[1].split("',")[0]
                    cnt_vol = textJson.split("'total_file_size': '")[1].split("',")[0]
                    fileNanem = "'file_name':"+' "'
                    if textJson.find(fileNanem) != -1:
                        cnt_fname = textJson.split(fileNanem)[1].split('",')[0]
                    else:
                        cnt_fname = textJson.split("'file_name': '")[1].split("',")[0]
                    jehu = textJson.split("'is_rights': '")[1].split("',")[0]
                    if jehu == 'Y':
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileguri',
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

    print("m_fileguri 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_fileguri 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
