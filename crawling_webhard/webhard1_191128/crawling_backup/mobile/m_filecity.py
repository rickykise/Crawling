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

def startCrawling(site):
    conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    i = 0;a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'etc': '',
                'idx': '',
                'pn': i,
                's_value': '',
                'tab': site,
                'tab2': '',
                'type': 'mobile',
                'view': 'list'
            }
            link = 'https://m.filecity.kr/module/contents_list.php'
            post_one  = s.post(link, data=Page)
            content = post_one.content
            soup = bs(content.decode('euc-kr','replace'), 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    cnt_num = text.split('idx":"')[a].split('","')[0]
                    url = 'https://m.filecity.kr/contents/#tab='+site+'&view=list&idx='+cnt_num
                    cnt_vol = text.split('"size":"')[a].split('","')[0]
                    url2 = "https://filecity.kr/html/view2.html"
                    a = a+1
                    if a == 21:
                        a = 1
                        break

                    idx = {
                        'idx': cnt_num,
                        'link': 'list',
                        'type': 'layer'
                    }
                    post_two  = s.post(url2, data=idx)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    title = soup.find('div', 'cont_title').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = soup.find('li', 'point02').find('span', 'num').text.strip().replace(",","")
                    cnt_writer = soup.find('li', 'nickname').text.strip()
                    cnt_fname = soup.find('div', 'info_body').find('li', 'info01')['title']

                    if soup.find('ul', 'clearfix icon_alliance '):
                        cnt_chk =1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecity',
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

    print("m_filecity 크롤링 시작")
    site = ['BD_MV','BD_DM','BD_UC','BD_AN']
    for s in site:
        startCrawling(s)
    print("m_filecity 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
