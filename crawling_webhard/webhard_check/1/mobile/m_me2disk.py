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

            data = {
                'cName': 'boardList',
                'cate1': site,
                'page': str(i)
            }
            link = 'http://m.me2disk.com/_module/board.enroll.php'
            post_one  = s.post(link, headers=headers, data=data)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    if a == 11:
                        a = 1
                        break
                    adult = text.split('<emadult>')[a].split('</')[0]
                    if adult == 'Y':
                        continue
                    cnt_num = text.split('<idx>')[a].split('</idx>')[0]
                    url = 'http://m.me2disk.com/?doc=board_view&idx='+cnt_num
                    a = a+1

                    post_two  = s.get(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    div = soup.find('div', 'vimgbx2')
                    cnt_chk = 0

                    title = soup.find('li', 'vtit_txt').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword(conn,curs)
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = div.find_all('span', 'mar_left10')[1].text.replace(",","").split("P")[0].strip()
                    if div.find_all('span', 'mar_left10')[1].find('img'):
                        jehu = div.find_all('span', 'mar_left10')[1].find('img')['src']
                        if jehu.find('affily') != -1:
                            cnt_chk = 1
                    cnt_writer = div.find_all('span', 'mar_left10')[2].text.replace(",","").split("P")[0].strip()
                    cnt_vol = div.find_all('span', 'mar_left10')[3].text.replace(",","").split("P")[0].strip()
                    cnt_fname = soup.find('div', 'vfile_txt').text.strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'me2disk',
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

    print("m_me2disk 크롤링 시작")
    site = ['MVO','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("m_me2disk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
