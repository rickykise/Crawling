import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;a = 0;b = 0;check = True;pageToken = '';videoIdCheck = ''
    client_secret = 'AIzaSyD72ge4xvWIZrg8PmJCQtIbKXfWQWCp8-U'
    channel_id = 'UUJP3wXQgncv59DcG0yjzRaw'
    link = 'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2CcontentDetails&maxResults=50&playlistId='+channel_id+'&key='+client_secret
    link2 = '&pageToken='
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            r = requests.get(link)
        else:
            r = requests.get(link+link2+pageToken)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        pageToken = text.split('nextPageToken": "')[1].split('",')[0]
        try:
            for item in text:
                if b == 100:
                    a = 0
                    b = 0
                    break
                a = a+1
                b = b+2
                videoId = text.split('videoId": "')[b].split('"')[0]
                if videoId == videoIdCheck:
                    continue
                videoIdCheck = videoId
                title = text.split('title": "')[a].split('"')[0].replace("\\n","").replace("\t","").replace("\xa0", "").replace("\\","")
                if title == '':
                    title = text.split('title": ')[1].split(',"description"')[0]
                    title = title[1:]
                    title = title[:-1]
                title = remove_emoji(title)
                title_null = titleNull(title)

                # 키워드 체크
                if title_null.find('야인시대') == -1:
                    continue
                cnt_id = '11709'
                cnt_keyword = '1034'
                cnt_keyword_nat = 'KR'

                url = 'https://www.youtube.com/watch?v='+videoId

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'youtube',
                    'cnt_title': title,
                    'cnt_title_null': title_null,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'unitedstates',
                    'cnt_writer': '',
                    'origin_url': '',
                    'origin_osp': '',
                    'cnt_keyword_nat': cnt_keyword_nat
                }
                # print(data)
                # print("=================================")

                dbResult = insertALLKey(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("youtube_channels 크롤링 시작")
    startCrawling()
    print("youtube_channels 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
