import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    with requests.Session() as s:
        a = 0;check = True
        searchKey = urllib.parse.quote_plus(keyword)
        now = datetime.datetime.now().strftime('%H:%M:%S')
        
        client_secret = 'AIzaSyCMsJX59IEw90y18PW3PfSItj3BVSGu620'

        url = 'https://www.googleapis.com/youtube/v3/search?q='+searchKey+'&part=snippet&key='+client_secret+'&maxResults=10&sp=CAISAhAB&part=snippet&order=date'
        post_one  = s.get(url)
        soup = bs(post_one.text, 'html.parser')
        text = str(soup)
        try:
            for item in text:
                if a == 50:
                    a = 1
                    break
                a = a+1
                videoId = text.split('videoId": "')[a].split('"')[0]
                cnt_writer = text.split('channelTitle": "')[a].split('"')[0]
                # cnt_writer 체크
                writerGet = getWriter()
                writerCheck = checkWriter(cnt_writer, writerGet)
                if writerCheck['m'] != None:
                    continue
                url2 = 'https://www.googleapis.com/youtube/v3/videos?id='+videoId+'&key='+client_secret+'&part=snippet,contentDetails,statistics,status'
                post_two  = s.get(url2)
                c = post_two.content
                soup2 = bs(c.decode('utf8','replace'), 'html.parser')
                text2 = str(soup2)

                title = text2.split('title": "')[1].split('"')[0].replace("\\n","").replace("\t","").replace("\xa0", "").replace("\\","")
                if title == '':
                    title = text2.split('title": ')[1].split(',"description"')[0]
                    title = title[1:]
                    title = title[:-1]
                title = remove_emoji(title)
                title_null = titleNull(title)
                googleCheck = googleCheckTitle(title_null, key, cnt_id)
                if googleCheck == None:
                    continue
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
                    'cnt_writer': cnt_writer,
                    'origin_url': '',
                    'origin_osp': '',
                    'cnt_keyword_nat': k_nat
                }
                print(data)
                print("=================================")

                # dbResult = insertALLKey(data)
        except:
            pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getKeywordDaily()

    print("youtube_api 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("youtube_api 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")


# 유튜브 글쓴이 가져오는 함수
def getWriter():
    with conn.cursor() as curs:
        sql = "SELECT cnt_writer FROM youtube_check;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def checkWriter(cnt_writer, writerGet):
    returnValue = {
        'm' : None
    }

    for u in writerGet:
        if cnt_writer.find(u) != -1 :
            returnValue['m'] = u

    return returnValue
