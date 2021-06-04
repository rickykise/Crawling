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
        'Cookie': 'SUNSSID=8u3csqfqkj3kr6sht2vv9299i0; _ga=GA1.2.439868459.1552550776; _gid=GA1.2.1483016532.1552550776; _gat=1; goToWork=0; exceptadult=1; wcs_bt=d26c6bfdca2be0:1552551732',
        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.filesun.com/disk/board.php?board='+site+'&page='+str(i)+'&exceptadult=1'
            post_one  = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'viewListArticle').find_all('li')

            try:
                for item in li:
                    text = str(item)
                    url = 'http://m.filesun.com'+item.find('a')['href']
                    cnt_num = url.split("&n=")[1].split("&")[0]
                    if url.find('&page') != -1:
                        url = url.split('&page')[0]
                    cnt_price = text.split('class="red">')[1].split('</')[0].replace(",","").replace("P","").strip()
                    url2 = 'http://www.filesun.com'+item.find('a')['href']

                    post_two  = s.get(url2)
                    soup2 = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup2.find('title').text.strip().split(" 다운로드")[0]
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue

                    if soup2.find('img', 'allianceicon'):
                        cnt_chk = 1
                    cnt_vol = soup2.find('td', 'size').text.strip().replace(" ","")
                    cnt_writer = soup2.find('td', colspan='2').text.strip().replace(" ","")
                    if cnt_writer.find('평가없음') != -1:
                        cnt_writer = cnt_writer.replace('\t', '').split('평가')[1].strip()
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
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("m_filesun 크롤링 시작")
    site = ['1&listmode=all','1','2','3','5']
    for s in site:
        startCrawling(s)
    print("m_filesun 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
