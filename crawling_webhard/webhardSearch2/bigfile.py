
import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling(key):
    i = 0; b = 1;check = True
    print(key)
    encText = urllib.parse.quote(key)
    link = "http://www.bigfile.co.kr/content/ajax_db_exod.php?sEg=Y&pg="
    link2 = "&total_count=563&outmax=20&s_field=S_TOTAL&searchWord="+encText
    while check:
        i = i+1
        if i == 4:
            break
        r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find_all("tr")
        if len(tr) < 2:
            check = False
            print("게시물없음\n========================")
            break

        try:
            for item in tr:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                td = item.find_all('td')
                if len(td) == 1:
                    continue

                img = item.find_all('td')[2].find_all('img')
                if len(img) == 1:
                    adult = item.find_all('td')[2].find('img')['src']
                    if adult.find('adult') != -1:
                        continue
                elif len(img) == 2:
                    adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                    adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                    if adult1.find('adult') != -1 or adult2.find('adult') != -1:
                        continue
                elif len(img) == 3:
                    adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                    adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                    adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                    if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1:
                        continue
                elif len(img) == 4:
                    adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                    adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                    adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                    adult4 = item.find_all('td')[2].find_all('img')[3]['src']
                    if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1 or adult4.find('adult') != -1:
                        continue
                elif len(img) == 5:
                    adult1 = item.find_all('td')[2].find_all('img')[0]['src']
                    adult2 = item.find_all('td')[2].find_all('img')[1]['src']
                    adult3 = item.find_all('td')[2].find_all('img')[2]['src']
                    adult4 = item.find_all('td')[2].find_all('img')[3]['src']
                    adult5 = item.find_all('td')[2].find_all('img')[4]['src']
                    if adult1.find('adult') != -1 or adult2.find('adult') != -1 or adult3.find('adult') != -1 or adult4.find('adult') != -1 or adult5.find('adult') != -1:
                        continue

                title = item.find('a')['title']
                title_null = titleNull(title)
                urlCh = item.find('a')['href'].split("('")[1].split("','")[0]
                cnt_chk = 0
                if title.find('요청자료') != -1:
                    title = item.find_all('a')[1]['title']
                    title_null = titleNull(title)
                    urlCh = item.find_all('a')[1]['href'].split("('")[1].split("','")[0]
                elif title.find('제휴업체') != -1:
                    title = item.find_all('a')[1]['title']
                    title_null = titleNull(title)
                    urlCh = item.find_all('a')[1]['href'].split("('")[1].split("','")[0]
                    cnt_chk = 1
                cnt_num = item.find('td', 'conlist_s').text.strip()
                url = 'http://www.bigfile.co.kr/content/content_sub.php?co_id='+cnt_num
                urlSub = 'http://www.bigfile.co.kr/content/content_main.php?co_id='+cnt_num
                # 키워드 체크
                # getKey = getKeyword()
                # keyCheck = checkTitle(title_null, getKey)
                # if keyCheck['m'] == None:
                #     dbResult = insertDB('bigfile',title,title_null,urlSub)
                #     continue
                # keyCheck2 = checkTitle2(title_null, getKey)
                # if keyCheck2['m'] == None:
                #     dbResult = insertDB('bigfile',title,title_null,urlSub)
                #     continue
                r = requests.get(url)
                r = requests.get(url, cookies = {'addOpenedCookie':'co_id'})
                c = r.content
                tags = BeautifulSoup(c,"html.parser")
                cnt_price = tags.find('li', 'gm ar02').text.split(" 캐시")[0].replace(",","").strip()
                cnt_vol = tags.find('li', 'gm ar03').text.split(" 용량")[0].strip()
                cnt_writer = tags.find('li', 'gm ar04').text.split(" 등록자")[0].strip()
                cnt_fname = tags.find('div', 'pp_fileinfo').find('td')['title']

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'bigfile',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': urlSub,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_regdate' : now,
                    'Cnt_chk': cnt_chk
                }
                # print(data)
                # print('========================================')

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("bigfile 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("bigfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
