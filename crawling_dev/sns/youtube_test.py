import requests,re
import pymysql,time,datetime
import urllib.parse
from snsFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date, timedelta

def getContents(url):
    r = requests.get(url)
    c = r.content
    tags = BeautifulSoup(c,"html.parser")
    print(tags)

    writer = tags.find('div', 'style-scope ytd-video-secondary-info-renderer').find('a')['aria-label'].strip()
    dateCheck = tags.find('span', 'date style-scope ytd-video-secondary-info-renderer').text.strip().split("게시일: ")[1]
    datetime.datetime.strptime(dateCheck, "%Y. %m. %d.").strftime('%Y. %m. %d.')
    date = datetime.datetime.strptime(dateCheck, "%Y. %m. %d.").strftime('%Y-%m-%d %H:%M:%S')
    text = tags.find('div', id='content').text.strip().replace("\n","").replace("\t","").replace("\xa0", "")
    if tags.find('span', 'view-count style-scope yt-view-count-renderer').text.strip() == '조회수 없음':
        view_cnt = 0
    else:
        view = tags.find('span', 'view-count style-scope yt-view-count-renderer').text.strip().split("조회수 ")[1].split("회")[0]
        view_cnt = int(''.join(list(filter(str.isdigit,view))))
    if tags.find('yt-formatted-string', 'style-scope ytd-message-renderer') != None:
        if tags.find('yt-formatted-string', 'style-scope ytd-message-renderer').text.strip() == '댓글을 달 수 없는 동영상입니다.':
            reply_cnt = 0
    else:
        reply = tags.find('div', 'style-scope ytd-comments-header-renderer').text.strip().split("댓글 ")[1].split("개")[0]
        reply_cnt = int(''.join(list(filter(str.isdigit,reply))))
    # reply = tags.find('div', 'style-scope ytd-comments-header-renderer').text.strip().split("댓글 ")[1].split("개")[0]
    # reply_cnt = int(''.join(list(filter(str.isdigit,reply))))
    if tags.find('yt-formatted-string', 'style-scope ytd-toggle-button-renderer style-text')['aria-label'] == '좋아요 없음':
        like_cnt = 0
    else:
        like = tags.find('yt-formatted-string', 'style-scope ytd-toggle-button-renderer style-text')['aria-label'].split("좋아요 ")[1].split("개")[0]
        like_cnt = int(''.join(list(filter(str.isdigit,like))))

    data = {
        'sns_content': text,
        'writeDate':  date,
        'sns_writer': writer,
        'like_cnt': like_cnt,
        'reply_cnt': reply_cnt,
        'view_cnt': view_cnt
    }

    return data

def startCrawling(key):
    print("키워드 : ",key)
    updateNum = 0;insertNum = 0
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        i = 0;
        link = "https://www.youtube.com/results?search_query="+key+"&sp=CAJCBAgBEgA%253D"
        # link = "https://www.youtube.com/results?search_query=류준열&sp=CAJCBAgBEgA%253D"
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        driver.set_window_position(0, 0)
        driver.set_window_size(1210, 1050)
        time.sleep(2)
        html = driver.find_element_by_id("contents").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        # div = soup.find('div', 'contents')
        ytd = soup.find_all("div", id="title-wrapper")
        # print(div)

        for item in ytd:
            # curs = conn.cursor(pymysql.cursors.DictCursor)
            # putKey = getPutKeyword(text,dbKey[key]['add'])
            # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if item.find('h3', id='video-title'):
                continue
            elif item.find('h3', 'title-and-badge'):
                title = item.find('h3', 'title-and-badge').text.strip()
                url = 'https://www.youtube.com'+item.find('h3', 'title-and-badge').find('a')['href']
                resultData = getContents(url)

            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            conn2 = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                putKey = getPutKeyword(text,dbKey[key]['add'])
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'sns_name': 'youtube',
                    'sns_title': title,
                    'sns_content': resultData['sns_content'],
                    'url': url,
                    'title_key': dbKey[key]['add'][0],
                    'keyword' : putKey,
                    'writeDate':  resultData['writeDate'],
                    'sns_writer': resultData['sns_writer'],
                    'like_cnt': resultData['like_cnt'],
                    'share_cnt': 0,
                    'reply_cnt': resultData['reply_cnt'],
                    'view_cnt': resultData['view_cnt'],
                    'createDate': now,
                    'updateDate': now
                }
                print(data)
                yester = datetime.datetime.now() - timedelta(1)
                yesterday = yester.strftime('%Y-%m-%d')
                if data['writeDate'] < yesterday: break
                # if date < datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'): break
                # if date < '2018-07-23 00:00:00': break

                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
                conn.commit()
                curs2.execute(sql, list(data.values()))
                conns.commit()
                insertNum = insertNum+1
            except Exception as e:
                # if e.args[0] == 1062: break
                if e.args[0] == 1062:
                    sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, updateDate=%s WHERE url=%s;"
                    curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                    updateNum = updateNum+1
                else:
                    pass
            finally:
                conn.close()
                conn2.close()
    # except:
    #     pass
    finally:
        driver.close()

    print("insert : ",insertNum,"/update :",updateNum)
    print("=======================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("youtube 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '마약왕':
        #     startCrawling(k)
        startCrawling(k)
    print("youtube 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
