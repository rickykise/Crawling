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
    i = 0;check = True;cnt_osp = 'babatv';cnt_url = 'https://drama14.babatv.club/'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        header_url = group_url[:-1]
        header_url = header_url.split('//')[1].strip()
        link = group_url+'bbs/board.php?bo_table='+site+'&page='
        cnt_osp = group_id
    else:
        link = 'https://drama14.babatv.club/bbs/board.php?bo_table='+site+'&page='
        header_url = cnt_url[:-1]
        header_url = header_url.split('//')[1].strip()
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('ul', 'fz_list').find_all('div', 'fz_subject')

        try:
            for item in div:
                if item.find('a'):
                    url = item.find('a')['href']
                    if url.find('&page') != -1:
                        url = url.split('&page')[0].strip()
                    url = urllib.parse.unquote(url)
                    title = item.find('a').text.strip()
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
                        bo = host_url.split('bo=')[1].split('&')[0]

                        Data = {
                            'bo': bo,
                            'id': id
                        }
                        headers = {
                            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'ko-KR',
                            'Cookie': 'ck_font_resize_add_class=; e1192aefb64683cc97abb83c71057733=ZHJhbWFfbmV3; ck_font_resize_rmv_class=; 2a0d2363701f23f8a75028924a3af643=MTcyLjY4LjE0NC4xNzA%3D; PHPSESSID=ptf7bff10vbv8k2ju05nrdgk12; _gid=GA1.2.233402756.1569992665; _ga=GA1.2.600144520.1569992665; __cfduid=dd726d76c36a2e9cb70d459ccaea77d9c1569992659; _gat_gtag_UA_88492110_22=1',
                            'Host': header_url,
                            'Referer': host_url,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                        }

                        with requests.Session() as s:
                            post_one  = s.get(host_url, headers=headers, data=Data)
                            content = post_one.content
                            soup = bs(content.decode('utf8','replace'), 'html.parser')
                            text = str(soup)
                            host_url = text.split('window.location.href="')[1].split('";')[0]

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
                                'cnt_writer': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)

        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("babatv 크롤링 시작")
    site = ['enter', 'enter_new', 'drama', 'drama_new']
    for s in site:
        startCrawling(s)
    print("babatv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
