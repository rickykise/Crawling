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
    link = 'https://iq5.zalba.club/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'fz_list').find_all('li')

        try:
            for item in li:
                cnt_num = item.find('div', 'fz_num').text.strip()
                if cnt_num == '번호' or cnt_num == 'AD':
                    continue
                url = item.find('div', 'fz_subject').find('a')['href']
                if url.find('&page=') != -1:
                    url = url.split('&page')[0]
                title = item.find('div', 'fz_subject').find('a').text.strip()
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

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', id='movie_bt')

                for item in div:

                    downCheck = item.text.strip()
                    if downCheck.find('다운로드') != -1:
                        continue
                    host_url = item.find('a')['href']
                    id = host_url.split('id=')[1].split('&')[0]
                    bo = host_url.split('bo=')[1]
                    Data = {
                        'bo': bo,
                        'id': id
                    }

                    headers = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cookie': '_ga=GA1.2.1409494417.1569996818; __cfduid=d44180300ab518c234f32d04f009b402a1569996814; _gid=GA1.2.1836968200.1571019712; _gat_gtag_UA_88492110_21=1; PHPSESSID=t8dvcv5irva3c1us3ea13f2eu5; ck_font_resize_rmv_class=; ck_font_resize_add_class=; e1192aefb64683cc97abb83c71057733=ZHJhbWFfbmV3',
                        'Host': 'iq5.zalba.club',
                        'Referer': host_url,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                    }

                    with requests.Session() as s:
                        post_one  = s.get(host_url, headers=headers, data=Data)
                        content = post_one.content
                        soup = bs(content.decode('utf8','replace'), 'html.parser')
                        text = str(soup)
                        host_url = text.split('window.location.href="')[1].split('";')[0]

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        origin_url = soup.find('iframe')['src']

                        if origin_url.find('https') == -1:
                            origin_url = 'https:'+origin_url
                        origin_osp = origin_url.split('//')[1]
                        if origin_osp.find('www') != -1:
                            origin_osp = origin_osp.split('www.')[1].split('.')[0]
                        else:
                            origin_osp = origin_osp.split('.')[0]

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'iq5.zalba',
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

    print("iq5.zalba 크롤링 시작")
    site = ['drama_new', 'enter_new', 'drama', 'enter']
    for s in site:
        startCrawling(s)
    print("iq5.zalba 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
