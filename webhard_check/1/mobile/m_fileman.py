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

def startCrawling(site):
    conn = host
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.fileman.co.kr/index.html?page='+str(i)+'&category1='+site+'&category2=&s_column=&s_word='
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', 'mobile_contents_txt')

            try:
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
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
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

    print("m_fileman 크롤링 시작")
    site = ['','MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_fileman 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
