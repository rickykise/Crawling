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

def startCrawling():
    i = 0;a = 1;check = True
    link = 'http://bongngotv.vip/phim-han-quoc/trang-'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'col-sm-6')

        try:
            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('div', 'inner').text.strip()
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

                seo = url.split('phim/')[1].strip()
                total = soup.find('aside', 'widget').find_all('li')[1].text.split(':')[1].strip()
                vid = soup.find('div', id=re.compile("comment-+"))['id'].split('comment-')[1].strip()

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Cache-Control': 'no-cache',
                    'Connection': 'Keep-Alive',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie': '__cfduid=d5e547f64a33faa778b22b521da9af7061593134605; _ga=GA1.2.1018008992.1593134608; _gid=GA1.2.311203495.1593134608; _gat=1',
                    'Host': 'ep.bongngotv.vip',
                    'Referer': 'http://bongngotv.vip/xem/'+seo,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                }

                Data = {
                    'seo': seo,
                    'tap': '1',
                    'total': total,
                    'vid': vid
                }

                sub_url = 'http://ep.bongngotv.vip/subitems'
                r = requests.post(sub_url, headers=headers, data=Data)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = str(soup).replace('\\', '')

                for item in text:
                    host_url = text.split('href='+"'"+'"')[a].split('"')[0]
                    title = titleSub + '_' + host_url.split("tap-")[1].strip()
                    title_null = titleNull(title)
                    a = a+1

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'bongngotv',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except:
            a = 1
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("bongngotv 크롤링 시작")
    startCrawling()
    print("bongngotv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
