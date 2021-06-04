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

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cache-Control': 'no-cache',
    'Connection': 'Keep-Alive',
    'Content-Length': '93',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '_ga=GA1.2.628962327.1552612222; _gid=GA1.2.426691868.1552612222; _gat=1; SellerPage=1; MylistPage=1; wcs_bt=s_419e761a640c:1552620767',
    'Host': 'm.fileham.com',
    'Referer': 'http://m.fileham.com/mobile/storage.php',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
    'X-Requested-With': 'XMLHttpRequest'
}

def startCrawling(site):
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.fileham.com/mobile/storage.php'
            Page = {
                'Limit': '10',
                'Page': str(i),
                'Search': '',
                'SearchKey': '',
                'act': 'load_list_page',
                'listorder': 'new',
                'mSec': site,
                'relate': '',
                'sSec': 'all'
            }
            post_one  = s.post(link, headers=headers, data=Page)
            soup = bs(post_one.text, 'html.parser')
            div = soup.find_all('div', 'ctn_tot')

            try:
                for item in div:
                    if item.find('div', 'adt_cover'):
                        continue
                    cnt_num = item['data-idx']
                    cnt_price = item.find_all('span')[4].text.replace(",","").split("P")[0].strip()
                    # cnt_vol = item.find_all('span')[3].text.strip()
                    url = 'http://m.fileham.com/mobile/storage.php?act=view&idx='+cnt_num

                    post_two  = s.get(url)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('li', 'vtit_txt').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_vol = soup.find_all('span', 'mar_left10')[2].text.strip()
                    cnt_writer = soup.find('div', 'vimgbx2').find_all('td')[2].text.split("판매자")[1].strip()
                    cnt_fname = soup.find('div', 'vfile_txt').text.strip()
                    if soup.find('span', 'vp_img_evt'):
                        jehu = soup.find('span', 'vp_img_evt').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileham',
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

    print("m_fileham 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_fileham 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
