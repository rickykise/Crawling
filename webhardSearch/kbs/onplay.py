import requests,re
import pymysql,time,datetime
import urllib.parse
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key):
    i = 0; a = 1;check = True
    print(key)
    encText = urllib.parse.quote(key)
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break

            Data = {
                'ba': '0',
                'c': '90000',
                'is_mobile': '0',
                'k': encText,
                'l': '20',
                'm': '0',
                'page': i,
                's': '0',
                'sk': 'S',
                'st': 'D'
            }

            headers = {
                'Accept': 'text/html, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': 'onplay.co.kr',
                'Referer': 'https://onplay.co.kr/search/?lo=0&fc=&k='+encText,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'X-Requested-With': 'XMLHttpRequest'
            }

            ajax_url = 'https://onplay.co.kr/ajax.php/search/ajax_get_search_contents_list/'
            try:
                r  = s.post(ajax_url, headers=headers, data=Data)
                c = r.content
                soup = BeautifulSoup(c.decode('unicode_escape','replace'),"html.parser")
                text = str(soup)
                json_obj = json.loads(text)
                result = json_obj['result']
                search_data = result['search_data']
                contents_list = search_data['contents_list']
                
                for item in contents_list:
                    adult = item['flag_adult']
                    if adult == '1':
                        continue
                    cnt_num = item['bbs_idx']
                    url = 'https://onplay.co.kr/search/?lo=0&fc=&k='+key+'#!action=contents&link=search&idx='+str(cnt_num)
                    cnt_price = item['contents_price']
                    cnt_vol = item['show_contents_size']
                    cnt_writer = item['seller_nickname']
                    title = item['show_title']
                    title_null = titleNull(title)
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    Data = {
                        'bbs_id': str(cnt_num),
                        'link': 'search',
                        's_page': str(i),
                        'search': encText,
                        'type': 'modal'
                    }

                    headers = {
                        'Accept': 'text/html, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cache-Control': 'no-cache',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'onplay.co.kr',
                        'Referer': 'https://onplay.co.kr/search/?lo=0&fc=&k='+encText,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'X-Requested-With': 'XMLHttpRequest'
                    }

                    ajax_url2 = 'https://onplay.co.kr/ajax.php/contents/modal/'+str(cnt_num)
                    post_two  = s.post(ajax_url2, data=Data, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    cnt_fname = soup.find('span', 'f_name').text.strip()
                    jehu = soup.find('div', 'v_file_info_wrap').find('td', 'con t5')
                    if jehu.find('span', 'a_ico'):
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'onplay',
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

    print("onplay 크롤링 시작")
    for k in getKey:
        startCrawling(k)
    print("onplay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
