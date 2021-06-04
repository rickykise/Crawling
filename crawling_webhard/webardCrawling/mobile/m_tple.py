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
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'code1': site,
                'code2': '',
                'copyrightIdx': '',
                'currentListScale': '0',
                'flagMore': '0',
                'flagPriceSupport': '',
                'hideAdult': '0',
                'hideCopyright': '0',
                'listObjID': 'contentsList',
                'listScale': '10',
                'listType': 'S',
                'pageNo': i,
                'searchValue': '',
                'todo': 'listAjax'
            }
            link = 'http://m.tple.co.kr/index.php'
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', onclick=re.compile("goViewPage+"))

            try:
                for item in div:
                    cnt_num = item['onclick'].split("goViewPage('")[1].split("',")[0]
                    url = 'http://m.tple.co.kr/?todo=storageView&idx='+cnt_num
                    url2 = 'http://www.tple.co.kr/storage/index.php?todo=view&source=W&idx='+cnt_num
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    PageSub = {
                        'bbsIdx': cnt_num,
                        'source': 'W',
                        'todo': 'viewBbsInfoAjax'
                    }

                    write_url = 'http://www.tple.co.kr/_renew/storage.php'
                    post_one  = s.post(write_url, data=PageSub)
                    write_tags = bs(post_one.text, 'html.parser')
                    write_text = str(write_tags)
                    cnt_writer = write_text.split('nickName":"')[1].split('","')[0].strip()

                    Page = {
                        'idx': cnt_num,
                        'source': 'W',
                        'todo': 'viewFile'
                    }
                    url3 = 'http://www.tple.co.kr/storage/index.php'

                    cnt_chk = 0
                    post_two  = s.post(url3, data=Page)
                    tags2 = bs(post_two.text, 'html.parser')
                    cnt_price = tags2.find('td', 'textRight').text.strip().split("P")[0].replace(",","")
                    cnt_vol = tags2.find_all('td', 'textRight')[1].text.strip()

                    if tags2.find('td', 'textLeft').find('img'):
                        cnt_chk = 1

                    fname = tags2.find('td', 'textLeft').find('span')['alt']
                    format1 = tags2.find('td', 'textLeft').find('span').text.strip()
                    if format1 == '':
                        fname = tags2.find_all('td', 'textLeft')[1].find('span')['alt']
                        format1 = tags2.find_all('td', 'textLeft')[1].find('span').text.strip()
                        format2 = tags2.find_all('td', 'textLeft')[1].text.strip().split(format1)[1]
                    else:
                        format2 = tags2.find('td', 'textLeft').text.strip().split(format1)[1]
                    fname = fname+format2

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'tple',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_tple 크롤링 시작")
    site = ['','1','2','4']
    for s in site:
        startCrawling(s)
    print("m_tple 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
