#트위터 크롤링 소스
import tweepy
import pymysql
import datetime,time,pytz
from snsFun import *
from bs4 import BeautifulSoup
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions

# 크롤링 함수
def startCrawling(key):
    print("키워드 : ",key)
    location = "%s,%s,%s" % ("35.95", "128.25", "1000km")
    checkDay = datetime.date.today() - datetime.timedelta(1)
    cursor = tweepy.Cursor(api.search,q=key+"-filter:retweets",geocode=location,include_entities=False,result_type='recent')# twitter 검색 cursor 선언
    updateNum = 0;insertNum = 0;i=1

    for i,tweet in enumerate(cursor.items()):
        try:
            text = tweet.text.replace("\t"," ").replace("\n"," ")
            url = 'https://twitter.com/'+tweet.user.screen_name+'/status/'+str(tweet.id)
            reply = '0'
            like = str(tweet.favorite_count)
            retwee = str(tweet.retweet_count)
            text = str(tweet.text).replace('\n', '')
            writeDate = str(tweet.created_at)

            if text.find("RT @") != -1: continue
            result = checkKeyword(text,dbKey[key]['add'],dbKey[key]['del'])
            if result:
                # if count['date'] < checkDay.strftime('%Y-%m-%d'): break
                if writeDate < '2020-06-01': break

                putKey = getPutKeyword(text,dbKey[key]['add'])
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'sns_name': 'twitter',
                    'sns_title': remove_emoji(tweet.user.name)+"#"+(putKey.replace("#","")), #제목
                    'sns_content': remove_emoji(text), # 내용
                    'url': url, # url
                    'title_key': dbKey[key]['add'][0],
                    'keyword': putKey, # 키워드
                    'writeDate': writeDate, # 날짜
                    'sns_writer': remove_emoji(tweet.user.name), # 글쓴이
                    'like_cnt': like, # 좋아요 수
                    'share_cnt': retwee, # 공유 수
                    'reply_cnt': reply, # 댓글 수
                    'createDate': now,
                    'updateDate': now
                }
                # print(data)
                # print("==============================")

                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
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
        except:
            continue

# 메인
if __name__=='__main__':
    start_time = time.time()
    # 트위터 계정
    consumer_key = "mEQMCnJFCLspWdeY0PeB9qgWs"
    consumer_secret = "1cNCN6XOkfFBNiKnGiMY4u6i9esF1ooEvVU6eKzR1mqtdRjYwZ"
    access_token = "4807917050-o6b971jVfXlXHcn9Nbj2HUIxCqTx2Up5NKHBfFl"
    access_token_secret = "RFDwVHSUUCdzd3aFjXzEeSatXnRQDshcg9IbSWJ55oFY8"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True , wait_on_rate_limit_notify = True)

    # 키워드 가져오기
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    # 크롤링 시작
    print("트위터 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("트위터 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
