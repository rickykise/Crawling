import requests, re
import pymysql, time, datetime
import urllib.parse
import sys, os
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


headers = {
    'Accept': 'text/html,  application/xhtml+xml,  image/jxr,  */*',
    'Accept-Encoding': 'gzip,  deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': '__cfduid=d12c382102db09e54373c4526f196c2ce1615167647; _ga=GA1.2.2095432199.1615167648; _gid=GA1.2.1276430576.1615167648; XSRF-TOKEN=eyJpdiI6Im9RdVg5eHppYWZiZG5oU2tOd01PZ2c9PSIsInZhbHVlIjoiQU5aV0JkUEo2TE53ZzZUamRFMzlSRk1yUHVtV0daOWNkNFU1ZDhyWk5JRnBvSzRnNVE1SFQ0UHJtREZuNkkwWFZkOXdhcW5XUnBSNlVvMWxrbFBhb2c9PSIsIm1hYyI6ImQyZDhlYWM0YmQ3NjJjZDgxYWU0OTYxODA1NTdhMTQ5ZWQ1YmNiY2U1MzlkNmFiYWExZGUzNGVjNzg5NjFhZWEifQ%3D%3D; laravel_session=eyJpdiI6InA0MGhvSlFoRFAwR1l4S3JVcVZwVFE9PSIsInZhbHVlIjoiREEwQkVLcjVRRXBJdUNFV0NwaHdhamxjeHlpNFFOM1BZd0ZQVjBKTmJSbmlsc0xGOHRCankzMGtBZ0pkaGJWc1dQQ1dkdnByTStPUGJQNlpBdndWQnc9PSIsIm1hYyI6IjM4MGM0MDVmNGI2YmZlNGM2ZWQwM2E3MzJjNDhhMTZiNThhZTdjMWIyMDAwMjE2NmQ3NDYxZGRmZTQyNWY0YjUifQ%3D%3D; AdskeeperStorage=%7B%220%22%3A%7B%7D%2C%22C786431%22%3A%7B%22page%22%3A1%2C%22time%22%3A1615168363954%7D%7D',
    'referer': 'https://hahaseries.com/category/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling():
    i = 0;check = True
    link = 'https://hahaseries.com/category/%E0%B8%8B%E0%B8%B5%E0%B8%A3%E0%B8%B5%E0%B9%88%E0%B8%A2%E0%B9%8C%E0%B9%80%E0%B8%81%E0%B8%B2%E0%B8%AB%E0%B8%A5%E0%B8%B5?page='
    while check:
        i = i+1
        if i == 13:
            break
        r = requests.get(link+str(i),  headers=headers)
        c = r.text
        soup = BeautifulSoup(c, "html.parser")
        div = soup.find_all('div',  'movie')
        # print(c)
        try:
            for item in div:
                url = item.find('a')['href']
                url = urllib.parse.unquote(url)
                titleSub = item.find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url,  headers=headers)
                c = r.text
                soup = BeautifulSoup(c, "html.parser")
                div = soup.find_all('div',  'episode')

                for item in div:
                    host_url = item.find('div')['data-href']
                    title = item.find('div')['data-ep-name']
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'hahaseries',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("hahaseries 크롤링 시작")
    startCrawling()
    print("hahaseries 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
