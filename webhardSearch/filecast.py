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
    i = 0; a = 1;check = True
    print(key)
    encText = urllib.parse.quote(key)
    link = 'https://www.filecast.co.kr/www/search/action/'
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            Page = {
                'category': '0',
                'first_load': '0',
                'is_category_list': '0',
                'limit': '20',
                'location': '0',
                'page': i,
                'page_load': '0',
                'search': encText,
                'seller': '',
                'sort_order': 'sort'
            }

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Connection': 'Keep-Alive',
                'Content-Length': '133',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie': 'user_temp_key=1589942156517896; d0b2bfbba204f3efa9b2b2b7ec36985a=MeuwlTLsnbw%3D; a73f1f772da9c87f89f6e68b2fc61ada=c29ydA%3D%3D; 47831f4e2d05a4f0b0f317b43844b932=MjA%3D; SERVERID=www2; fc_adult=2020-05-20%2011%3A08%3A30; fc_user_access_token=false',
                'Host': 'www.filecast.co.kr',
                'Referer': 'https://www.filecast.co.kr/www/search/?category=0&location=0&search='+encText,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest',
            }
            r = s.post(link, data=Page, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)

            try:
                for item in text:
                    if a == 15:
                        a = 1
                    cnt_num = text.split('"idx":"')[a].split('","')[0]
                    adult = text.split('flag_adult":"')[a].split('","')[0]
                    if adult == "1":
                        continue
                    url = 'http://filecast.co.kr/www/contents/view/'+cnt_num
                    urlSub = 'http://www.filecast.co.kr/www/contents/view/'+cnt_num+'/1/'
                    cnt_chk = 0

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    title = soup.find('span', 'txt').text.strip()
                    title_null = titleNull(title)

                    cnt_price = soup.find('span', 'txt_blue txt_block').find('b').text.replace(",","").strip()
                    cnt_writer = soup.find('a', 'btn_memo')['onclick'].split("('")[1].split("')")[0]
                    cnt_vol = soup.find('li', 'l4').find('span', 'txt_block').text.replace(" ","").strip()
                    cnt_fname = soup.find('span', 'file_name').text.strip()
                    ico = soup.find('span', 'ico_partner')['class']
                    lenico = len(ico)
                    if lenico == 2:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filecast',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': urlSub,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)

                    a = a+1
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("filecast 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filecast 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
