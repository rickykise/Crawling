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
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def startCrawling(site):
    conn = host
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.filehon.com/index.php?page='+str(i)+'&doc=board_list&cate1='+site+'&cate2='
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'conlist').find_all('li')
            try:
                for item in li:
                    cnt_chk = 0
                    text = str(item)
                    if text.find('19금') != -1:
                        continue
                    if text.find('제휴') != -1:
                        cnt_chk = 1
                    url = 'http://m.filehon.com'+item.find('a')['href']
                    cnt_num = url.split("&idx=")[1].split("&")[0]

                    post_one  = s.post(url, headers=headers)
                    soup = bs(post_one.text, 'html.parser')

                    title = soup.find('div', 'title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('p', 'movie_price').text.split("가격")[1].split("P")[0].replace(",","").strip()
                    cnt_vol = soup.find('span', 'detail').text.split("원본크기:")[1].strip()
                    cnt_writer = soup.find('p', 'movie_uploader').text.split("등록자:")[1].strip()
                    cnt_fname = soup.find('ul', 'file_list').find('li').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filehon',
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

    print("m_filehon 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filehon 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
