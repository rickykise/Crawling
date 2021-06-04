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

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer': 'http://m.ondisk.co.kr',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break

            link = 'http://m.ondisk.co.kr/api/content/list.php?cate='+site+'&search_type=title&is_rights=y&adult_not=y&page='+str(i)
            post_one  = s.post(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    cnt_num = text.split('"idx":')[a].split(',')[0]
                    url = 'http://m.ondisk.co.kr/?cate='+site+'&idx='+cnt_num
                    url2 = 'http://m.ondisk.co.kr/api/content/view.php?idx='+cnt_num

                    a = a+1
                    if a == 76:
                        a = 1
                        break

                    post_two  = s.post(url2, headers=headers).json()
                    textJson = str(post_two)
                    # post_two  = s.post(url2, headers=headers)
                    # content = post_two.content
                    # soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    # textJ = str(soup).split()
                    # jsonString = json.loads(textJ)
                    # textJson = str(jsonString)
                    cnt_chk = 0

                    title = textJson.split("'title': '")[1].split("',")[0]
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
                        'Cnt_osp' : 'ondisk',
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

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_ondisk 크롤링 시작")
    site = ['ALL','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_ondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
