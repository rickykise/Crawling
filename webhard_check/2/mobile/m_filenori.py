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
    'Cookie': 'JSESSIONID=037D42999513B9AFF91DB9E57C331A9B; mEventDesignVer=1060',
    'Host': 'm.filenori.com',
    'Referer': 'http://m.filenori.com/Mobile/home.do',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
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
            link = 'http://m.filenori.com/Mobile/Contents/list.do?st=1&mc='+site+'&pp='+str(i)
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('utf-8','replace'), 'html.parser')
            div = soup.find('div', id='contentsList').find_all('div', 'nContentView')

            try:
                for item in div:
                    adult = item['data'].split('|')[3]
                    if adult == '1':
                        continue
                    cnt_num = item['data'].split('|')[0]
                    title = item.find('span', 'titie').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    url = 'http://m.filenori.com/Mobile/Contents/view.do?cID='+cnt_num

                    post_two  = s.get(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('utf-8','replace'), 'html.parser')
                    cnt_chk = 0

                    cnt_price = soup.find('span', id='contentsPrice').text.split('캐시')[0].replace(',', '').strip()
                    cnt_writer = soup.find('span', 'regUser').text.strip()
                    cnt_vol = soup.find('div', 'list_title').text.split('/')[1].split('/')[0].strip()
                    cnt_fname = soup.find('div', 'box_fileinfo_last').find('li', 'info_title').text.strip()
                    if soup.find('span', 'pshipIcon'):
                        jehu = soup.find('span', 'pshipIcon').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filenori',
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

    print("m_filenori 크롤링 시작")
    site = ['00','01','02','03','05']
    for s in site:
        startCrawling(s)
    print("m_filenori 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
