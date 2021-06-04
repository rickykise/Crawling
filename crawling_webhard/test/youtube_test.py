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

# db에 널을 text setting
def setText(s,t):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&apos;", "'")
    s = s.replace("&amp;", "&")
    s = s.replace("<b>","")
    s = s.replace("</b>","")
    s = s.replace("\r","")

    if t == 0:
        s = (len(s) > 49) and s[:47]+"…" or s
        s = remove_emoji(s)

    return s

#이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

def startCrawling(key):
    print("키워드 : ",key)
    with requests.Session() as s:
        a = 0;check = True
        key = urllib.parse.quote_plus(key)
        url = 'https://www.googleapis.com/youtube/v3/search?q='+key+'&part=snippet&key=AIzaSyDmgHZcv-cP-8iZlCpS1ZKkUGHzT4mNjxo&maxResults=50&sp=CAISAhAB&part=snippet&order=date'

        post_one  = s.get(url)
        soup = bs(post_one.text, 'html.parser')
        text = str(soup)
        print(text)
        for item in text:
            try:
                if a == 50:
                    a = 1
                    break
                a = a+1
                videoId = text.split('videoId": "')[a].split('"')[0]
                url2 = 'https://www.googleapis.com/youtube/v3/videos?id='+videoId+'&key=AIzaSyDmgHZcv-cP-8iZlCpS1ZKkUGHzT4mNjxo&maxResults=2&part=snippet,contentDetails,statistics,status'
                post_two  = s.get(url2)
                c = post_two.content
                soup2 = bs(c.decode('utf8','replace'), 'html.parser')
                text2 = str(soup2)
                print(text2)

                title = text2.split('title": "')[1].split('"')[0].replace("\\n","").replace("\t","").replace("\xa0", "").replace("\\","")

                title = remove_emoji(title)
                print(title)
                description = text2.split('description": "')[1].split('"')[0]
                description = setText(description,0).replace("\\n","").replace("\t","").replace("\xa0", "").replace("\\","")
                url = 'https://www.youtube.com/watch?v='+videoId
                date = text2.split('publishedAt": "')[1].split('T')[0]
                dateTime = text2.split(date+'T')[1].split('.')[0]
                writeDate = date+' '+dateTime
                writer = text2.split('channelTitle": "')[1].split('"')[0]
                like_cnt = text2.split('likeCount": "')[1].split('"')[0]
                dislike_cnt = text2.split('dislikeCount": "')[1].split('"')[0]
                reply_cnt = text2.split('commentCount": "')[1].split('"')[0]
                view_cnt = text2.split('viewCount": "')[1].split('"')[0]


                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                conn2 = pymysql.connect(host='192.168.0.12',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(text,dbKey[key]['add'])
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = {
                        'sns_name': 'youtube',
                        'sns_title': title,
                        'sns_content': description,
                        'url': url,
                        'title_key': dbKey[key]['add'][0],
                        'keyword' : putKey,
                        'writeDate':  writeDate,
                        'sns_writer': writer,
                        'like_cnt': like_cnt,
                        'share_cnt': dislike_cnt,
                        'reply_cnt': reply_cnt,
                        'view_cnt': view_cnt
                    }
                    if data['keyword'] == '':
                        data['keyword'] = data['title_key']
                    print(data)
                    print('=========================================')

                #     placeholders = ', '.join(['%s'] * len(data))
                #     columns = ', '.join(data.keys())
                #     sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                #     curs.execute(sql, list(data.values()))
                #     conn.commit()
                #     curs2.execute(sql, list(data.values()))
                #     conn2.commit()
                #     insertNum = insertNum+1
                # except Exception as e:
                #     # if e.args[0] == 1062: break
                #     if e.args[0] == 1062:
                #         sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, updateDate=%s WHERE url=%s;"
                #         curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                #         curs2.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                #         updateNum = updateNum+1
                #     else:
                #         pass
                finally:
                    conn.close()
                    conn2.close()
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
