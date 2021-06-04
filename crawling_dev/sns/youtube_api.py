import requests,re
import pymysql,time,datetime
import urllib.parse
from snsFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from urllib import parse

def startCrawling(key):
    print("키워드 : ",key)
    with requests.Session() as s:
        a = 0;check = True
        searchKey = urllib.parse.quote_plus(key)
        now = datetime.datetime.now().strftime('%H:%M:%S')
        if now > '18:00:00':
            client_secret = 'AIzaSyDmgHZcv-cP-8iZlCpS1ZKkUGHzT4mNjxo'
        else:
            client_secret = 'AIzaSyAHDYCkeyP1t-MciNwL8D_1UqS5O1zHgN8'


        # client_secret = 'AIzaSyDE-cLxUC88Q03u9KR1FnXk1OIZ99sX0-A'
        url = 'https://www.googleapis.com/youtube/v3/search?q='+searchKey+'&part=snippet&key='+client_secret+'&maxResults=10&sp=CAISAhAB&part=snippet&order=date'
        post_one  = s.get(url)
        soup = bs(post_one.text, 'html.parser')
        text = str(soup)

        for item in text:
            try:
                if a == 50:
                    a = 1
                    break
                a = a+1
                videoId = text.split('videoId": "')[a].split('"')[0]
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
                description = text2.split('description": "')[1].split('"')[0]
                description = setText(description,0).replace("\\n","").replace("\t","").replace("\xa0", "").replace("\\","")
                url = 'https://www.youtube.com/watch?v='+videoId
                date = text2.split('publishedAt": "')[1].split('T')[0]
                dateTime = text2.split(date+'T')[1].split('Z')[0]
                writeDate = date+' '+dateTime
                writer = text2.split('channelTitle": "')[1].split('"')[0]
                like_cnt = text2.split('likeCount": "')[1].split('"')[0]
                dislike_cnt = text2.split('dislikeCount": "')[1].split('"')[0]

                if text2.find('commentCount') != -1:
                    reply_cnt = text2.split('commentCount": "')[1].split('"')[0]
                else:
                    reply_cnt = 0
                view_cnt = text2.split('viewCount": "')[1].split('"')[0]
                putKey = getPutKeyword(description,dbKey[key]['add'])


                data = {
                    'sns_title': title,
                    'sns_content': description,
                    'url': url,
                    'title_key': dbKey[key]['add'][0],
                    'keyword' : key,
                    'writeDate':  writeDate,
                    'sns_writer': writer,
                    'like_cnt': like_cnt,
                    'share_cnt': dislike_cnt,
                    'reply_cnt': reply_cnt,
                    'view_cnt': view_cnt
                }
                print(data)
                print("=================================")

                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    dbResult = insert(conn,data['sns_title'],data['sns_content'],data['url'],data['title_key'],data['keyword'],data['writeDate'],data['sns_writer'],data['like_cnt'],data['share_cnt'],data['reply_cnt'],data['view_cnt'])
                except Exception as e:
                    print(e)
                    pass
                finally :
                    conn.close()
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("youtube_api 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("youtube_api 크롤링 끝")

    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
