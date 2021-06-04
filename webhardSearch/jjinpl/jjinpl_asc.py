import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    i = 0;check = True;first_t = '';check_i = 0
    print(key)
    encText = urllib.parse.quote(key)
    link = 'http://www.jjinpl.com/contents/board.php?menu=1&menumode=all&sf=subject&sw='+encText+'&page='
    while check:
        i = i+1
        check_i = 0
        print(str(i))
        if i == 30:
            break
        try:
            r = requests.get(link+str(i))
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            if soup.find('div', 'thumb'):
                li = soup.find('div', 'thumb').find('ul').find_all('li')

                for item in li:
                    cnt_num = item['class'][1].split('thumbnail')[0].strip()
                    url = 'http://www.jjinpl.com'+item.find('a')['href']
                    title = item.find('label', 'mainchecklabel').text.strip()
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

                    cnt_vol = item.find('p', 'tbs_s').text.replace(' ', '').replace(",","").strip()
                    cnt_price = item.find('p', 'tbs_p').text.replace(" ","").replace(",","").split("P")[0].strip()
                    if cnt_price.find('→') != -1:
                        cnt_price = cnt_price.split('→')[1].strip()

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    title = soup.find('table', 'infoSheet').find('td', colspan="5").text.strip()
                    title_null = titleNull(title)
                    cnt_writer = soup.find_all('td', colspan="3")[2].text.strip()
                    if cnt_writer.find('평가없음') != -1:
                        cnt_writer = cnt_writer.split('\t')[0].strip()
                    cnt_fname = soup.find('div', 'filelist').find('table', 'infoSheet').find('tbody').find('td', colspan="7").text.strip()

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

            else:
                check=False;break
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("jjinpl 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("jjinpl 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
