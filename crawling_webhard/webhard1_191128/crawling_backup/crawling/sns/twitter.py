#트위터 크롤링 소스
import tweepy
import pymysql
import datetime,time,pytz
from snsFun import *
from bs4 import BeautifulSoup
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions

# 날짜 처리 함수
def settingDate(date):
    date = date.replace("년",".").replace("월",".").replace("일","").replace(" ","").replace("\n","").split("-")
    time = date[0]
    tmpDate = date[1]

    if date[0][0:2] == '오전':
        temp = date[0].split("오전")[1].split(":")
        if temp[0] == '12': temp[0] = '00'
        tmpDate = tmpDate+" "+temp[0]+":"+temp[1]
    elif date[0][0:2] == '오후':
        temp = date[0].split("오후")[1].split(":")
        if temp[0] == '12': temp[0] = '00'
        tmpDate = tmpDate+" "+str(int(temp[0])+12)+":"+temp[1]

    returnDate = datetime.datetime.strptime(tmpDate,"%Y.%m.%d %H:%M") + datetime.timedelta(hours=17)
    # print(tmpDate,returnDate)
    return returnDate

# 공유,댓글,좋아요 수 크롤링 함수
def getCount(url):
    try:
        s = Session()
        s.mount('https://twitter.com/', HTTPAdapter(max_retries=Retry(total=5, status_forcelist=[500, 503])))
        r = s.get(url)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        item = soup.find("div","permalink-tweet-container")

        reply = item.find("div",{"class":"ProfileTweet-action--reply"})
        like = item.find("div",{"class":"ProfileTweet-action--favorite"})
        retwee = item.find("div",{"class":"ProfileTweet-action--retweet"})
        date = item.find("div",{"class","client-and-actions"})

        likeNum = like.find("span",{"class":"ProfileTweet-actionCountForPresentation"}).text
        replyNum = reply.find("span",{"class":"ProfileTweet-actionCountForPresentation"}).text
        retweeNum = retwee.find("span",{"class":"ProfileTweet-actionCountForPresentation"}).text
        dateSpan = date.find("span",{"class","metadata"})
        metadata = settingDate(dateSpan.find_all("span",limit=1)[0].text)
        data = {
            'likeNum': (likeNum != '') and int(''.join(list(filter(str.isdigit,likeNum)))) or 0,
            'replyNum': (replyNum != '') and int(''.join(list(filter(str.isdigit,replyNum)))) or 0,
            'retweeNum': (retweeNum != '') and int(''.join(list(filter(str.isdigit,retweeNum)))) or 0,
            'date': metadata
        }
        return data
    except Exception as e:
        print("에러:",e,url)
        data = {'likeNum': 0,'replyNum': 0,'retweeNum': 0,'date': ''}
        return data

# 크롤링 함수
def startCrawling(key):
    print("키워드 : ",key)
    location = "%s,%s,%s" % ("35.95", "128.25", "1000km")
    checkDay = datetime.date.today() - datetime.timedelta(1)
    cursor = tweepy.Cursor(api.search,q=key+"-filter:retweets",geocode=location,include_entities=False,result_type='recent')# twitter 검색 cursor 선언
    updateNum = 0;insertNum = 0;i=1
    for i,tweet in enumerate(cursor.items()):
        text = tweet.text.replace("\t"," ").replace("\n"," ")
        url = 'https://twitter.com/'+tweet.user.screen_name+'/status/'+str(tweet.id)
        print(url)
        if text.find("RT @") != -1: continue
        result = checkKeyword(text,dbKey[key]['add'],dbKey[key]['del'])
        if result:
            count = getCount(url)
            if count['date'] == '' or count['date'].strftime('%H:%M:%S') == '00:00:00': continue
            if count['date'].strftime('%Y-%m-%d') < checkDay.strftime('%Y-%m-%d'): print(count['date']);break

            putKey = getPutKeyword(text,dbKey[key]['add'])
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {
                'sns_name': 'twitter',
                'sns_title': remove_emoji(tweet.user.name)+"#"+(putKey.replace("#","")), #제목
                'sns_content': remove_emoji(text), # 내용
                'url': url, # url
                'title_key': dbKey[key]['add'][0],
                'keyword': putKey, # 키워드
                'writeDate': count['date'], # 날짜
                'sns_writer': remove_emoji(tweet.user.name), # 글쓴이
                'like_cnt': count['likeNum'], # 좋아요 수
                'share_cnt': (count['retweeNum'] != 0) and count['retweeNum'] or tweet.retweet_count, # 공유 수
                'reply_cnt': count['replyNum'], # 댓글 수
                'createDate': now,
                'updateDate': now
            }
            # print(data['writeDate'])

            # conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            # try:
            #     curs = conn.cursor(pymysql.cursors.DictCursor)
            #     placeholders = ', '.join(['%s'] * len(data))
            #     columns = ', '.join(data.keys())
            #     sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
            #     curs.execute(sql, list(data.values()))
            #     insertNum = insertNum+1
            # except Exception as e:
            #     if e.args[0] == 1062:
            #         sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, share_cnt=%s, updateDate=%s WHERE url=%s;"
            #         curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
            #         updateNum = updateNum+1
            #     else:
            #         print("DB에러:",e)
            # else:
            #     conn.commit()
            # finally:
            #     conn.close()

    print("insert : ",insertNum,"/update :",updateNum)
    print("=======================")


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
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    # 크롤링 시작
    print("트위터 크롤링 시작")
    for k in dbKey.keys():
        startCrawling(k)
    print("트위터 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
