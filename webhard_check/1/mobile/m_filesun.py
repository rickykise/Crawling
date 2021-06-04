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
global host

headers = {
        'Cookie': 'SUNSSID=8u3csqfqkj3kr6sht2vv9299i0; _ga=GA1.2.439868459.1552550776; _gid=GA1.2.1483016532.1552550776; _gat=1; goToWork=0; exceptadult=1; wcs_bt=d26c6bfdca2be0:1552551732',
        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
    }

def startCrawling(site):
    conn = host
    curs = conn.cursor(pymysql.cursors.DictCursor)
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
                    cnt_price = text.split('class="red">')[1].split('</')[0].replace(",","").strip()
                    url2 = 'http://www.filesun.com'+item.find('a')['href']

                    post_two  = s.get(url2)
                    soup2 = bs(post_two.text, 'html.parser')

                    title = soup2.find('title').text.strip().split(" 다운로드")[0]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_vol = soup2.find('td', 'size').text.strip().replace(" ","")

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

                    conn2 = host
                    try:
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        dbResult = insert(conn2,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
                    except Exception as e:
                        print(e)
                        pass
                    finally :
                        conn2.close()
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
