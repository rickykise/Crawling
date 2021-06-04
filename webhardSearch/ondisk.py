import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        i = 0;a = 0;check = True
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://ondisk.co.kr/main/module/bbs_list_sphinx_prc.php?mode=ondisk&list_row=20&page='
            link2 = '&search_type=ALL&search_type2=title&sub_sec=&search='+encText+'&hide_adult=Y&blind_rights=N&sort_type=&sm_search=&plans_idx='
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                'Referer': 'http://ondisk.co.kr/index.php?mode=ondisk&search_type=ALL&sub_sec=undefined',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cookie': 'list_type=mnShare_text_list; js-formlist-layer=true; _ga=GA1.3.1508842954.1547455426; _gid=GA1.3.604540773.1547455426; topBnnrSlide_20150715=true; app_version=0; Intro_domain_chk=ondisk.co.kr; keep_query_string=%2Findex.php%3Fmode%3Dondisk%26search_type%3DMVO%26sub_sec%3Dundefined; keep_search_type=ALL'
            }
            sys.setrecursionlimit (2000)
            post_one  = s.post(link+str(i)+link2, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            idx_arr = text.split('idx_arr":')[1].split(',')[0]
            if idx_arr == "null":
                continue
            idx = str(','+text.split('idx_arr":"')[1].split('","')[0]+',')

            try:
                for item in idx:
                    if a == 21:
                        a = 1
                        break
                    a = a+1
                    cnt_num = idx.split(',')[a].split('","')[0]
                    url = 'http://ondisk.co.kr/pop.php?sm=bbs_info&idx=' + cnt_num

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    textS = str(soup)
                    cnt_chk = 0

                    if soup.find('div', id='loadingBar') or textS.find('성인인증') != -1 or textS.find('잘못된 접근') != -1:
                        continue
                    else:
                        title = soup.find('span', 'tit_txt').text.replace("\n","").replace("\t","").replace("\xa0", "").replace(" ", "").strip()
                        title_null = titleNull(title)

                        cnt_writer = soup.find('div', 'sellerCredit').find('a').text.strip()
                        cnt_vol = soup.find('table', 'ctvTbl').find('tbody').find_all('td')[1].text.strip()
                        cnt_price = soup.find('strong', 'ctvTblPoint').text.strip().replace(",","")
                        span = soup.find('div', 'bxSkin').find('ul').find('li').find('span').text.strip()
                        cnt_fname = soup.find('div', 'bxSkin').find('ul').find('li').text.replace("\n","").replace("\t","").replace("\xa0", "").strip().split(span)[0]

                        if soup.find('div', 'ctvTitle').find('h2').find('img'):
                            img = soup.find('div', 'ctvTitle').find('h2').find('img')['src']
                            if img.find('icon_partnership') != -1:
                                cnt_chk = 1

                        data = {
                            'Cnt_num' : cnt_num,
                            'Cnt_osp' : 'ondisk',
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
                        # print("=================================")

                        dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKey(conn,curs)
    conn.close()

    print("ondisk 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("ondisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
