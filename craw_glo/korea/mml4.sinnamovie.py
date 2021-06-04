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
path = inspect.getfile(inspect.currentframe())
x = path.split('\\')
x.reverse()
osp_id = x[0].split('.py')[0].strip()

def startCrawling(site):
    i = 0;check = True;cnt_osp = 'mml4.sinnamovie'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        header_url = group_url[:-1]
        header_url = header_url.split('//')[1].strip()
        link = group_url+'bbs/board.php?bo_table='+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://mml4.sinnamovie.net/bbs/board.php?bo_table='+site+'&page='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        tr = soup.find('form', id='fboardlist').find('tbody').find_all('tr')

        try:
            for item in tr:
                url = item.find('a')['href']
                if url.find('&page') != -1:
                    url = url.split('&page')[0]
                title = item.find('a').text.strip()
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
                    check_down = item.find('a').text.strip()
                    if check_down.find('다운로드') != -1:
                        continue
                    url2 = item.find('a')['href']
                    bo = url2.split('bo=')[1]
                    id = url2.split('id=')[1].split('&')[0]

                    Data = {
                        'bo': bo,
                        'id': id
                    }
                    url2 = group_url+'player_url.php?id='+id+'&bo='+bo
                    headers = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cookie' : '__cfduid=d7b5eb1dfa321667e22793dc50a2152b01571031201; _ga=GA1.2.1414783521.1571031206; _gid=GA1.2.1971105276.1571031206; _gat_gtag_UA_88492110_36=1; PHPSESSID=9nj6kk8ugp0lkg9rjbf7s7oia6; e1192aefb64683cc97abb83c71057733=ZHJhbWFfbmV3; 2a0d2363701f23f8a75028924a3af643=MTYyLjE1OC4xMTkuOA%3D%3D; ck_font_resize_rmv_class=; ck_font_resize_add_class=',
                        'Host': header_url,
                        'Referer': url2,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                    }
                    with requests.Session() as s:
                        post_one  = s.post(url2, headers=headers, data=Data)
                        content = post_one.content
                        soup = bs(content.decode('utf8','replace'), 'html.parser')
                        text = str(soup)
                        host_url = text.split('window.location.href="')[1].split('";')[0]

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")

                        try:
                            origin_url = soup.find('iframe', id='vid_iframe')['src']

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
                            'cnt_osp' : cnt_osp,
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

    print("mml4.sinnamovie 크롤링 시작")
    site = ['enter_new', 'enter', 'drama_new', 'drama']
    for s in site:
        startCrawling(s)
    print("mml4.sinnamovie 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
