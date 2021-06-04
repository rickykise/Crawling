import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;check = True
    link = 'https://p.livemovies.net//bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'bo_subject')

        try:
            for item in div:
                url = item.find('a')['href']
                if url.find('&page') != -1:
                    url = url.split('&page')[0]
                title = item.find('a').text.strip()
                if title.find('N새글') != -1:
                    title = title.split('N새글')[0].strip()
                if title.find('새글') != -1:
                    title = title.split('새글')[0].strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']
                keyCheck2 = checkTitle2(title_null, getKey)
                if keyCheck2['m'] == None:
                    continue

                bo_table = url.split('bo_table=')[1].split('&')[0]
                wr_id = url.split('wr_id=')[1]

                Data = {
                    'bo_table': bo_table,
                    'wr_id': wr_id
                }
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Content-Length': '29',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie': '__cfduid=db9f198f45f256bf45047a8bfe2f1e3341570780793; _ga=GA1.2.574726034.1570780796; _gid=GA1.2.1006534797.1570780796; PHPSESSID=dvgl7oghha41gg7im8s4jcp9tl; e1192aefb64683cc97abb83c71057733=ZHJhbWFfbmV3; 2a0d2363701f23f8a75028924a3af643=MTcyLjY4LjQ2LjIyNA%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=',
                    'Host': 'p.livemovies.net/',
                    'Referer': url,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
                    'X-Requested-With': 'XMLHttpRequest'
                }

                with requests.Session() as s:
                    post_one  = s.post('https://p.livemovies.net//bbs/a_link_ajax.php', headers=headers, data=Data)
                    content = post_one.content
                    soup = bs(content.decode('utf8','replace'), 'html.parser')
                    div = soup.find_all('div', id='movie_bt')

                    for item in div:
                        bo = item.find_all('input')[1]['value']
                        id = item.find('input')['value']
                        Data2 = {
                            'bo': bo,
                            'id': id
                        }
                        headers2 = {
                            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'ko-KR',
                            'Cache-Control': 'no-cache',
                            'Content-Length': '22',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Cookie': '__cfduid=db9f198f45f256bf45047a8bfe2f1e3341570780793; _ga=GA1.2.574726034.1570780796; _gid=GA1.2.1006534797.1570780796; PHPSESSID=dvgl7oghha41gg7im8s4jcp9tl; e1192aefb64683cc97abb83c71057733=ZHJhbWFfbmV3; 2a0d2363701f23f8a75028924a3af643=MTcyLjY4LjQ2LjIyNA%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=',
                            'Host': 'p.livemovies.net/',
                            'Referer': url,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                        }
                        post_two  = s.post('https://p.livemovies.net//player_url.php', headers=headers2, data=Data2)
                        content = post_two.content
                        soup = bs(content.decode('utf8','replace'), 'html.parser')
                        text = str(soup)
                        host_url = text.split('window.location.href="')[1].split('";')[0]

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")

                        try:
                            origin_url = soup.find('iframe')['src']

                            if origin_url.find('https') == -1:
                                origin_url = 'https:'+origin_url
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]
                        except:
                            origin_url = ''
                            origin_osp = ''

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'p.livemovies',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'southkorea',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("p.livemovies 크롤링 시작")
    site = ['drama_new', 'drama', 'enter_new']
    for s in site:
        startCrawling(s)
    print("p.livemovies 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
