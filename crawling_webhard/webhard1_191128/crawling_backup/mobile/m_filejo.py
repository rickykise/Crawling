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
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 2:
                break
            print(site)
            link = "http://m.filejo.com/?c="+site+"#"+str(i)+"^osort^s"
            print(link)
            print('=============================================================')
            post_one  = s.get(link, headers=headers)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            div = soup.find_all('div', 'list')

            try:
                for item in div:
                    cnt_num = item.find('div', 'title').find('a')['href'].split("group_no=")[1]
                    url = 'http://m.filejo.com'+item.find('div', 'title').find('a')['href']

                    post_two  = s.post(url, headers=headers)
                    content = post_two.content
                    soup = bs(content.decode('euc-kr','replace'), 'html.parser')
                    text = str(soup)
                    div = soup.find('div', 'datatext')
                    cnt_chk = 0

                    title = soup.find('div', 'filetitle').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    label = div.find('ul').find_all('li')[2].find('label').text.strip()
                    if div.find('ul').find_all('li')[2].find('strike'):
                        cnt_price = div.find('ul').find_all('li')[2].find('font').text.strip().replace(",","").split('P')[0]
                    else:
                        cnt_price = div.find('ul').find_all('li')[2].text.split(label)[1].strip().replace(",","").split('P')[0]
                    if div.find('ul').find_all('li')[2].find('img'):
                        img = div.find('ul').find_all('li')[2].find_all('img')
                        if len(img) == 1:
                            jehu = div.find('ul').find_all('li')[2].find('img')['src']
                            if jehu.find('icon_affily') != -1:
                                cnt_chk = 1
                        elif len(img) == 2:
                            jehu1 = div.find('ul').find_all('li')[2].find_all('img')[0]['src']
                            jehu2 = div.find('ul').find_all('li')[2].find_all('img')[1]['src']
                            if jehu1.find('icon_affily') != -1 or jehu2.find('icon_affily') != -1:
                                cnt_chk = 1
                    cnt_writer = div.find('ul').find_all('li')[4].text.split('등록자')[1].strip()
                    cnt_vol = text.split("contents_size'><b>")[1].split("</b>")[0]
                    cnt_fname = soup.find('div', 'filelist').find('li').text.strip()
                    if soup.find('div', 'filelist').find('li').find('button'):
                        button = soup.find('div', 'filelist').find('li').find('button').text.strip()
                        cnt_fname = cnt_fname.split(button)[0]

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filejo',
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

                    conn2 = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
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

    print("m_filejo 크롤링 시작")
    site = ['MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_filejo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
