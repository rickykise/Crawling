import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

# 익스트림 url
def getUrl():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "SELECT url, news_idx, title_key, keyword FROM news_data where news_state = 1 and news_type in ('1', '2', '3') order by createDate desc;"
        # sql = "SELECT url, news_idx FROM news_data where news_state = 2 order by createDate desc limit 1;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
                returnValue[key].append(result[i][2])
                returnValue[key].append(result[i][3])
            else:
                returnValue.update({key:[result[i][1],result[i][2],result[i][3]]})
        # print(returnValue)

        return returnValue

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['news_idx'],data['reply_comm_num'],data['reply_content'],data['reply_writer'],data['writeDate'],data['title_key'],data['keyword'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'reply_data'
        data = {
            'news_idx': args[0],
            'reply_comm_num': args[1],
            'reply_content': args[2],
            'reply_writer' : args[3],
            'writeDate': args[4],
            'title_key': args[5],
            'keyword' : args[6],
            'createDate': now,
            'updateDate':now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            print("===========에러==========\n에러 : ",e,"\n",args,"\n===========에러==========")
        else:
            result = True
            conn.rollback()
    finally:
        return result

#이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

def startCrawling(url, keyItem):
    url = url; news_idx = keyItem[0]; title_key = keyItem[1]; keyword = keyItem[2]
    print(url)
    print("=================================")
    print("=================================")
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    article = soup.find_all('article', id=re.compile("comment_+"))

    # try:
    for item in article:
        reply_comm_num = item['id'].split('comment_')[1].strip()
        content = item.find('div', re.compile("comment_+")).text.strip()
        content = remove_emoji(content)
        writer = item.find('a', 'nickname').text.strip()
        dateCheck = item.find('span', 'ppcmt_date')['title']
        writeDate = datetime.datetime.strptime(dateCheck, "%Y.%m.%d. %H:%M").strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'news_idx' : news_idx,
            'reply_comm_num' : reply_comm_num,
            'reply_content' : content,
            'reply_writer' : writer,
            'writeDate' : writeDate,
            'title_key': title_key,
            'keyword' : keyword,
        }
        print(data)
        print("=================================")

        dbResult = insertALL(data)
    # except:
    #     pass

if __name__=='__main__':
    start_time = time.time()
    getUrl = getUrl()

    print("extmovie 크롤링 시작")
    for u, k in getUrl.items():
        startCrawling(u, k)
    print("extmovie 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
