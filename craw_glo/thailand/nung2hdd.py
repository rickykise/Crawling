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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

# headers = {
#     'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'ko-KR',
#     'Host': 'nung2hdd.co',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
# }

def startCrawling():
    i = 0;check = True
    link = 'https://www.nung2hdd.com/category/local-movies/korea-movies/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'moviebox')

        try:
            for item in div:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('img')['alt'].strip()
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find('ul', 'videoapi-list-episode').find_all('li', 'videoapi-episode')

                for item in li:
                    episode = item.find('span')['data-episode']
                    post_id = item.find('span')['data-post-id']
                    server =  item.find('span')['data-server']

                    data = {
                        'action': 'videoapi_get_player',
                        'episode': episode,
                        'post_id': post_id,
                        'server': server
                    }

                    ajax_url = 'https://www.nung2hdd.com/wp-admin/admin-ajax.php'

                    r = requests.post(ajax_url, data=data)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")

                    host_url = soup.find('iframe')['src']
                    title = titleSub+'_'+episode
                    title_null = titleNull(title)

                    origin_url = host_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'nung2hdd',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
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

    print("nung2hdd 크롤링 시작")
    startCrawling()
    print("nung2hdd 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
