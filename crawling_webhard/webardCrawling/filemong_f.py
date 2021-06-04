import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 2:
                break
            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'crossCookie=bar; PHPSESSID=ogiikktergbpef071apso79hv2',
                'Host': 'filemong.com',
                'Referer': 'https://filemong.com/?bs='+site,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest'
            }
            link = 'https://filemong.com/?bs='+site
            post_one  = s.post(link)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'content-list').find_all('li')

            try:
                for item in li:
                    title = item.find('strong', 'ctit').text.strip()
                    title_null = titleNull(title)
                    cnt_num = item.find('a', 'ctitle')['onclick'].split('page_open(')[1].split(',')[0].strip()
                    url = 'https://filemong.com/contents/info_ajax.php?bbs_idx='+cnt_num
                    cnt_price = item.find('div', 'pay').text.replace(",","").replace('P', '').strip()

                    # 키워드 체크
                    getKey = getKeywordNet()
                    keyCheck = checkTitleNet(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filemong',title, title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filemong',title, title_null,url)
                        continue
                    checkPrice = str(keyCheck['p'])

                    cnt_writer = item.find('div', 'name').text.strip()
                    cnt_vol = item.find('div', 'byte').text.strip()

                    Data = {
                        'bbs_idx': cnt_num
                    }

                    link2 = 'https://filemong.com/contents/info_ajax.php'
                    post_two  = s.post(link2, headers=headers, data=Data, allow_redirects=False)
                    soup2 = bs(post_two.text, 'html.parser')
                    cnt_chk = 0
                    cnt_fname = soup2.find('tbody', id='flist_s').find('td').text.strip()
                    if checkPrice == cnt_price:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemong',
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

    print("filemong 크롤링 시작")
    site = ['DRA', 'BCT']
    for s in site:
        startCrawling(s)
    print("filemong 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
