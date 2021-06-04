import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def siteCheck(osp_id, url):
    urlState = ''
    osp_id = osp_id.replace('.', '')
    try:
        result = osp_id+'Check(url)'
        return eval(result)
    except Exception as e:
        return urlState

def bilibiliCheck(url):
    urlState = ''
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR',
        'Connection': 'Keep-Alive',
        'Cookie': '_uuid=0BDAE319-FA31-2D45-8344-C08F7ECB1A2B25864infoc; buvid3=5EFCDA81-FF4A-4044-9CB5-8341A48CA4F9155829infoc; LIVE_BUVID=AUTO7815712060247214',
        'Host': 'search.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    try:
        r = requests.get(url, headers=headers)
        urlState = r.status_code

    except:
        pass

    return urlState

def bigdramasCheck(url):
    urlState = ''

    try:
        r = requests.get(url)
        urlState = r.status_code
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        title = soup.find('title').text.strip()
        if title.find('大劇獨播') != -1:
            urlState = 200
    except:
        pass

    return urlState

# def main():
#     cnt_id = 'bigdramas'
#     url = 'https://bigdramas.me'
#     data = siteCheck(cnt_id,url)
#     print(cnt_id)
#     print(data)
#
# if __name__=='__main__':
#     start_time = time.time()
#     main()
