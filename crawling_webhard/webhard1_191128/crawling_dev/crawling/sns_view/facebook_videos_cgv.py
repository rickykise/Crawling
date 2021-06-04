app_id = "902409216594778"
app_secret = "96f1b4f6cf119b6d2057100f19b47fd5"
access_token = app_id + "|" + app_secret
page_dic = {
    'CGV':'119682344771692'
    # '워버브러더스':'138228302942302',
    # '롯데시네마':'175770306139336',
    # '메가박스':'216047658463111',
    # 'MercedesBenzKorea':'301304903282392'
}

###
# 툼레이더
# 워버브러더스 : 1944655825607659
# 워버브러더스 : 1465860866845699
# CGV : 1500669616698157
###
from datetime import date, timedelta
today = date.today() + timedelta(1)
beforelast = date.today() - timedelta(days=2)

# since = beforelast.strftime('%Y-%m-%d')
# until = today.strftime('%Y-%m-%d')
# since = '2018-05-01'
# until = '2018-05-08'
# until = tomorrow.strftime('%Y-%m-%d')

from snsFun import *
import pymysql
conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
dbKey = getSearchKey(conn,curs)
conn.close()

# 조회수 가져오는 함수
import requests
import re
from bs4 import BeautifulSoup
def getLookup(url):
    r = requests.get(url)
    start = int(r.text.find('<div class="_1vx9"><span>조회'))
    soup = BeautifulSoup(r.text[start:start+100],"html.parser")
    num = None
    try:
        ele = [itme for itme in soup.find_all('span',class_=False)][0]
        num = re.sub('[^0-9]', '', ele.text)
    except:
        print(url,ele)

    return num

import time
import datetime
import urllib.request
def request_until_suceed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)  # wnat to know what error it is
            time.sleep(5)
            print("Error for url %s : %s" % (url, datetime.datetime.now()))

    return response.read().decode(response.headers.get_content_charset())

# advaced information
import json
def getFacebookPageFeedData(page_id, access_token):
    # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id
    parameters = "/feed?fields=link,message,created_time,shares,comments.limit(0).summary(true),likes.limit(0).summary(true)"

    access = "&access_token=%s" % access_token
    url = base + node + parameters + access
    print(url)
    data = json.loads(request_until_suceed(url))

    return data

def insert(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    data = {
        'sns_content' : args[0],
        'sns_writer' : pageName,
        'url' : args[1],
        'like_cnt' : args[2],
        'reply_cnt' : args[3],
        'share_cnt' : args[4],
        'view_cnt' : 0,
        'writeDate' : args[5],
        'title_key' : '',
        'keyword' : '',
        'keyword_type' : '',
        'createDate' : now,
        'updateDate' : now
    }
    data['view_cnt'] = getLookup(data['url'])
    print(data)

    mkey = getMainKeyword(dbKey,data['sns_content'])
    if mkey:
        data['title_key'] = dbKey['챔피언']['add'][0]
        data['keyword'] = getPutKeyword(data['sns_content'],dbKey['챔피언']['add'])

        if data['keyword']:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            data['keyword_type'] = getPutKeywordType(data['keyword'],conn,curs)
            data['keyword_type'] = (data['keyword_type'] == None) and '' or data['keyword_type']

    sqlUpdate = None;sqlInsert = None
    try:
        if data['keyword']:
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sqlInsert = "INSERT INTO facebook_videos ( %s ) VALUES ( %s );"  % (columns, placeholders)
            curs = conn.cursor(pymysql.cursors.DictCursor)
            curs.execute(sqlInsert, list(data.values()))
            conn.commit()
    except Exception as e:
        if e.args[0] != 1062:
            # sqlInsert = "INSERT INTO facebook_videos ( %s ) VALUES ( %s ) ON DUPLICATE KEY UPDATE like_cnt=\'"+data['like_cnt']+"\', reply_cnt=\'"+data['reply_cnt']+"\', share_cnt=\'"+data['share_cnt']+"\', view_cnt=\'"+data['view_cnt']+"\', updateDate=\'"+data['updateDate']+"\';"
            sqlInsert = "INSERT INTO facebook_videos ( %s ) VALUES ( %s );"  % (columns, placeholders)
            print("DB에러:",e)
            print("SQL:",sqlInsert,list(data.values()))
            print("data:",data)
            print("================")

    finally:
        conn.close()

def setDate(date):
    result = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+0000')
    result = result + datetime.timedelta(hours=+9)
    result = result.strftime('%Y-%m-%d %H:%M:%S')
    return result

def setContent(data):
    result = data.encode('cp949', errors= 'replace').decode('cp949')
    result = remove_emoji(result).strip().replace('\n',' ').replace('\t',' ')
    return result

def fetch_feed(pageKey):
    post_json = getFacebookPageFeedData(page_dic[pageKey], access_token)
    for idx,value in enumerate(post_json['data']):
        try:
            if ('description' in value) is False:
                value.update({'description':''})
            if ('link' in value) is False:
                value['link'] = 'https://www.facebook.com/'+pageKey+'/posts/'+value['id'].split('_')[1]
            if ('likes' in value) is False:
                value.update({'likes':{'summary':{'total_count':0}}})
            if ('comments' in value) is False:
                value.update({'comments':{'summary':{'total_count':0}}})
            if ('shares' in value) is False:
                value.update({'shares':{'count':0}})
            insert(pageKey,setContent(value['message']),value['link'],str(value['likes']['summary']['total_count']),str(value['comments']['summary']['total_count']),str(value['shares']['count']),setDate(value['created_time']))
            # if value['link'].find('/videos/') == -1:
            #     insert(pageKey,setContent(value['message']),value['link'],str(value['likes']['summary']['total_count']),str(value['comments']['summary']['total_count']),str(value['shares']['count']),setDate(value['created_time']))
        except Exception as e:
            print(type(e))
            print("('shares' in value) : ",('shares' in value))
            print('post_json에러:',e,'\n',value)
def main():
    start_time = time.time()
    for p in page_dic:
        print(p+" 크롤링")
        fetch_feed(p)
    print("--- %s seconds ---" %(time.time() - start_time))

if __name__ == '__main__':
    main()
