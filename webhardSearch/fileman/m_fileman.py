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
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=vdp7ctdanms3iqh6u5h7ngckf5; 07099283cfc31f2d473bf5b4628ab3a6=dXAwMDAx',
    'Host': 'm.fileman.co.kr',
    'Referer': 'http://m.fileman.co.kr/',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

headers2 = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=cc7prkncvotlnfidibd3cbcfd5; 07099283cfc31f2d473bf5b4628ab3a6=dXAwMDAx',
    'Host': 'fileman.co.kr',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key):
    i = 0;a = 1;check = True
    print('키워드 : '+key)
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 10:
                break
            print(str(i))
            try:
                encText = key.encode('euc-kr')
                encText = urllib.parse.quote(encText)
                link = 'http://m.fileman.co.kr/index.html?page='+str(i)+'&category1=&category2=&s_column=title&s_word='+encText
                post_one  = s.get(link, headers=headers)
                content = post_one.content
                soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                div = soup.find_all('div', 'mobile_contents_txt')
                if len(div) < 1:
                    break

                for item in div:
                    url = 'http://m.fileman.co.kr'+item.find('a')['href']
                    cnt_num = url.split("idx=")[1]

                    post_two  = s.get(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    text = str(soup)
                    if text.find('성인 인증후 이용하세요') != -1:
                        continue
                    title = soup.find('div', id='Content_Title').find('li').text.strip()
                    title_null = titleNull(title)
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    li = soup.find('li', 'Choice_Contents_Simple_Text').text.strip()
                    cnt_price = li.split("포인트")[1].split("P")[0].strip().replace(",","")
                    cnt_vol = li.split("(")[1].split(":")[0].strip()
                    cnt_writer = li.split("등록자")[1].strip()
                    cnt_fname = soup.find('li', 'Content_File_3').text.strip()

                    url2 = 'http://fileman.co.kr/contents/view_top.html?idx='+cnt_num+'&amp;page='
                    post_jehu  = s.get(url2, headers=headers2)
                    content = post_jehu.content
                    soup2 = bs(content.decode('euc-kr','replace'), 'html.parser')
                    cnt_chk = 0
                    text = str(soup2)
                    cnt_fname = soup2.find('span', 'font_layerlist').text.strip()
                    
                    if cnt_fname.find("/") != -1:
                        cnt_fname = soup2.find_all('span', 'font_layerlist')[1].text.strip()
                    if text.find('저작권자와의 제휴') != -1:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'fileman',
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
                    # print('======================')

                    dbResult = insertALLM(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("m_fileman 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("m_fileman 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
