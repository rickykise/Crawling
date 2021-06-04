import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from snsFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def getTime(date):

    dateGettime = date
    try:
        if dateGettime.find('오전 12:') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "오전 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d 00:%M:%S')
        elif dateGettime.find('오후 12:') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
        elif dateGettime.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
            clock = datetime.datetime.strptime(dateGettime, "오후 %H:%M - %Y년 %m월 %d일").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        else:
            writeDate = datetime.datetime.strptime(dateGettime, "오전 %H:%M - %Y년 %m월 %d일").strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    # print(writeDate)
    return writeDate

def getContents(url):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    reply = soup.find('div', 'ProfileTweet-action--reply').find('span', 'ProfileTweet-actionCountForPresentation').text.strip()
    if reply == '':
        reply = 0
    like = soup.find('div', 'ProfileTweet-action--favorite').find('span', 'ProfileTweet-actionCountForPresentation').text.strip()
    if like == '':
        like = 0
    share = soup.find('div', 'ProfileTweet-action--retweet').find('span', 'ProfileTweet-actionCountForPresentation').text.strip()
    if share == '':
        share = 0
    contents = soup.find('div', 'js-tweet-text-container').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
    if soup.find('div', 'js-tweet-text-container').find('a'):
        a = soup.find('div', 'js-tweet-text-container').find('a').text.strip()
        contents.split(a)[0]
    date = soup.find('span', 'metadata').find('span').text.strip()
    writeDate = getTime(date)

    data = {
        'reply': reply,
        'like': like,
        'share': share,
        'contents' : contents,
        'writeDate' : writeDate
    }
    # print(data)
    return data

def startCrawling(key):
    print("키워드 : ",key)
    i = 0;check = True
    updateNum = 0;insertNum = 0;
    checkDay = datetime.date.today() - datetime.timedelta(1)
    link = "https://twitter.com/search?f=tweets&vertical=default&q="+key+"&src=typd"
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        while check:
            driver.get(link)
            time.sleep(1)
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            html = driver.find_element_by_class_name("stream").get_attribute('innerHTML')
            soup = BeautifulSoup(html,'html.parser')
            li = soup.find("ol", id='stream-items-id').find_all("li", 'stream-item')

            for item in li:
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                writer = item.find('span', 'username').find('b').text.strip()
                url = 'https://twitter.com' + item.find('a', 'tweet-timestamp')['href']
                resultData = getContents(url)

                if resultData['contents'].find("RT @") != -1: continue
                result = checkKeyword(resultData['contents'],dbKey[key]['add'],dbKey[key]['del'])
                if result:
                    if resultData['writeDate'] < checkDay.strftime('%Y-%m-%d'):
                        check = False;break
                    putKey = getPutKeyword(resultData['contents'],dbKey[key]['add'])
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = {
                        'sns_name': 'twitter',
                        'sns_title': remove_emoji(writer)+"#"+(putKey.replace("#","")), #제목
                        'sns_content': remove_emoji(resultData['contents']), # 내용
                        'url': url, # url
                        'title_key': dbKey[key]['add'][0],
                        'keyword': putKey, # 키워드
                        'writeDate': resultData['writeDate'], # 날짜
                        'sns_writer': remove_emoji(writer), # 글쓴이
                        'like_cnt': resultData['like'], # 좋아요 수
                        'share_cnt': resultData['share'], # 공유 수
                        'reply_cnt': resultData['reply'], # 댓글 수
                        'createDate': now,
                        'updateDate': now
                    }
                    # print(data)
                    # print('============================================')

                    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
                    conn2 = pymysql.connect(host='14.52.95.199',user='overwaret',password='uni1004!',db='union',port=3307,charset='utf8')

                    try:
                        curs = conn.cursor(pymysql.cursors.DictCursor)
                        curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                        placeholders = ', '.join(['%s'] * len(data))
                        columns = ', '.join(data.keys())
                        sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                        curs.execute(sql, list(data.values()))
                        curs2.execute(sql, list(data.values()))
                        insertNum = insertNum+1
                    except Exception as e:
                        if e.args[0] == 1062:
                            sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, share_cnt=%s, updateDate=%s WHERE url=%s;"
                            curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
                            curs2.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
                            updateNum = updateNum+1
                        else:
                            print("DB에러:",e)
                    else:
                        conn.commit()
                        conn2.commit()
                    finally:
                        conn.close()
                        conn2.close()
            check = False;break

        print("insert : ",insertNum,"/update :",updateNum)
        print("=======================")
    except:
        pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    # 키워드 가져오기
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    # 크롤링 시작
    print("트위터 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '성난황소':
        #     startCrawling(k)
        startCrawling(k)
    print("트위터 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
