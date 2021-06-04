import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun_m import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

# replace('●', '')
def startCrawling(key):
    i = 0;check = True;first_t = '';check_i = 0
    print(key)
    encText = urllib.parse.quote(key)
    link = 'http://m.jjinpl.com/contents/board.php?menu=1&menumode=all&sf=subject&sw='+encText+'&page='
    with requests.Session() as s:
        while check:
            i = i+1
            check_i = 0
            print(str(i))
            if i == 30:
                break
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Cookie': 'exceptadult=1',
                'Host': 'm.jjinpl.com',
                'Referer': link+str(i),
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
            }
            try:
                post_one  = s.get(link+str(i), headers=headers)
                soup = bs(post_one.text, 'html.parser')
                li = soup.find('ul', id='articleSelectUl').find_all('li')

                for item in li:
                    url = 'http://m.jjinpl.com'+item.find('a')['href'].split('&page')[0].strip()
                    cnt_num = url.split('no=')[1].strip()
                    title = item.find('strong', 'subject').text.strip()
                    if check_i == 0:
                        if title == first_t:
                            check=False;break
                        else:
                            first_t = title
                            check_i = 1
                    title_null = titleNull(title)
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    cnt_vol = item.find('span', 'size').text.replace(' ', '').replace(',', '').strip()
                    cnt_price = item.find('span', 'price').text.replace(' ', '').replace(',', '').split('P')[0].strip()
                    if cnt_price.find('→') != -1:
                        cnt_price = cnt_price.split('→')[1].strip()

                    post_one  = s.get(url, headers=headers)
                    soup = bs(post_one.text, 'html.parser')

                    cnt_fname = soup.find('span', 'name').text.strip()
                    cnt_writer = soup.find('div', 'postInfo').find_all('tr')[1].find('td').text.strip()
                    if cnt_writer.find('평가없음') != -1:
                        cnt_writer = cnt_writer.split('평가없음')[0].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'jjinpl',
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
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("m_jjinpl 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("m_jjinpl 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
