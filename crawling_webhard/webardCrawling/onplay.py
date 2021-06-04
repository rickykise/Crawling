import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'https://onplay.co.kr/category/web/'+site+'/#!action=category&page='
            post_one  = s.get(link+str(i))
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'category-contents-list-data').find_all('li')

            try:
                for item in li:
                    adult = item.find('div')['data-adult'].strip()
                    if adult == '1':
                        continue
                    cnt_num = item.find('div')['data-idx'].strip()
                    url = link.split('#!action')[0]+'#!action=contents&link=category&idx='+cnt_num
                    title = item.find('div', 'l1').text.strip()
                    print(title)
                    title_null = titleNull(title)

                    # 키워드 체크
                    # getKey = getKeyword()
                    # keyCheck = checkTitle(title_null, getKey)
                    # if keyCheck['m'] == None:
                    #     dbResult = insertDB('onplay',title,title_null,url)
                    #     continue
                    # keyCheck2 = checkTitle2(title_null, getKey)
                    # if keyCheck2['m'] == None:
                    #     dbResult = insertDB('onplay',title,title_null,url)
                    #     continue

                    cnt_vol = item.find('div', 'l2').text.strip()
                    cnt_price = item.find('div', 'l3').text.replace(',', '').strip()
                    cnt_writer = item.find('div', 'l4')['data-name']

                    Data = {
                        'bbs_id': cnt_num,
                        's_page': str(i),
                        'search': '',
                        'type': 'modal'
                    }

                    headers = {
                        'Accept': 'text/html, */*; q=0.01',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cache-Control': 'no-cache',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Host': 'onplay.co.kr',
                        'Referer': link.split('#!action')[0],
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    ajax_url = 'https://onplay.co.kr/ajax.php/contents/modal/'+cnt_num
                    post_two  = s.post(ajax_url, data=Data, headers=headers)
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
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("onplay 크롤링 시작")
    site = ['11000','12000','13000']
    for s in site:
        startCrawling(s)
    print("onplay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
