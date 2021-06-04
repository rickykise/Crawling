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

def startCrawling(site):
    i = 0;check = True
    link = 'https://asianlist.net/genre/'+site+'/page/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', id=re.compile("post-+"))

        try:
            for item in article:
                url = item.find('div', 'data').find('a')['href']
                titleSub = item.find('div', 'data').find('a').text.strip()
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
                if soup.find('ul', 'episodios'):
                    li = soup.find('ul', 'episodios').find_all('li')

                    for item in li:
                        host_url = item.find('div', 'episodiotitle').find('a')['href']
                        title = item.find('div', 'episodiotitle').find('a').text.strip()
                        title_null = titleNull(title)

                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")

                        li = soup.find('div', id='playeroptions').find('ul').find_all('li')
                        for item in li:
                            host_link = 'https://asianlist.net/wp-admin/admin-ajax.php'
                            nume = item['data-nume']
                            post = item['data-post']
                            type = item['data-type']
                            data = {
                                'action': 'doo_player_ajax',
                                'nume': nume,
                                'post': post,
                                'type': type
                            }
                            r = requests.post(host_link, data=data)
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")

                            host_url = soup.find('iframe')['src'].strip()
                            if host_url == '' or host_url.find('kdramahood') != -1:
                                continue
                            if host_url.find('http') == -1:
                                host_url = 'https:'+host_url
                            if host_url.find('&sub=') != -1:
                                host_url = host_url.split('&sub=')[0]

                            origin_osp = host_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'asianlist',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'other',
                                'cnt_writer': '',
                                'origin_url': host_url,
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

    print("asianlist 크롤링 시작")
    site = ['korean-drama','kshows']
    for s in site:
        startCrawling(s)
    print("asianlist 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
