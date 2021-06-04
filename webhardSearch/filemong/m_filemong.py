import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    i = 0;check = True
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        while check:
            if i == 30:
                break
            Data = {
                'p': str(i),
                'search': key,
                'search_keyword': 'all',
                'search_type': 'all'
            }
            print(str(i))
            i = i+1
            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'm.filemong.com',
                'Referer': 'https://m.filemong.com/contents/list.html?search_type=all&search_keyword=all&search='+encText,
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                'X-Requested-With': 'XMLHttpRequest'
            }

            try:
                link = 'https://m.filemong.com/contents/search_ajax.php'
                post_one  = s.post(link, headers=headers, data=Data)
                soup = bs(post_one.text, 'html.parser')
                li = soup.find_all('li')
                if len(li) < 2:
                    print('게시글 없음')
                    break

                for item in li:
                    title = item.find('strong', 'ctit').text.strip()
                    title_null = titleNull(title)
                    cnt_num = item.find('a', 'content-item')['onclick'].split("page_open('")[1].split("')")[0].strip()
                    url = 'https://m.filemong.com/contents/view.html?idx='+cnt_num
                    cnt_price = item.find('div', 'text-pay').text.replace(",","").replace('P', '').strip()
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    post_one  = s.get(url, headers=headers)
                    soup = bs(post_one.text, 'html.parser')

                    cnt_fname = soup.find('tr', 'trShow_non').find('td').text.strip()
                    cnt_writer = soup.find('h1', 'hd-prof').text.strip()
                    cnt_chk = 0
                    if soup.find('span', 'badge0'):
                        jehu = soup.find('span', 'badge0').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filemong',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : '',
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALLM(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyAsc(conn,curs)
    conn.close()

    print("m_filemong 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("m_filemong 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
