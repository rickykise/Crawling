import re
import pymysql
import datetime

def insert(conn,pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'sns_content' : args[0],
        'sns_subcontent' : args[1],
        'sns_writer' : pageName,
        'url' : args[2],
        'like_cnt' : args[3],
        'reply_cnt' : args[4],
        'share_cnt' : args[5],
        'view_cnt' : args[6],
        'writeDate' : args[7],
        'title_key' : '',
        'keyword' : '',
        'keyword_type' : '',
        'createDate' : now,
        'updateDate' : now
    }

    sqlUpdate = None;sqlInsert = None
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sqlInsert = "INSERT INTO facebook_videos ( %s ) VALUES ( %s );" % (columns, placeholders)
    # sqlUpdate = "UPDATE facebook_post SET like_cnt=%s, reply_cnt=%s, share_cnt=%s, updateDate=%s WHERE url=%s;"

    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sqlInsert, list(data.values()))
        conn.commit()
    # except Exception as e:
        # if e.args[0] == 1062 and sqlUpdate:
        #     curs.execute(sqlUpdate,(data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
        # elif e.args[0] != 1062:
        #     print("DB에러:",e)
        #     print("SQL:",sqlInsert,list(data.values()))
        #     print("data:",data)

    finally:
        conn.close()

#페이스북 그래프
def insert2(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    data = {
        'sns_writer' : pageName,
        'url' : args[0],
        'view_cnt' : args[1],
        'like_cnt' : args[2],
        'reply_cnt' : args[3],
        'writeDate' : args[4],
        'createDate' : now,
        'updateDate' : now
    }

    sqlUpdate = None;sqlInsert = None
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sqlInsert = "INSERT INTO facebook_graph ( %s ) VALUES ( %s );" % (columns, placeholders)
    # sqlUpdate = "UPDATE facebook_post SET like_cnt=%s, reply_cnt=%s, share_cnt=%s, updateDate=%s WHERE url=%s;"

    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        curs.execute(sqlInsert, list(data.values()))
        conn.commit()
    # except Exception as e:
        # if e.args[0] == 1062 and sqlUpdate:
        #     curs.execute(sqlUpdate,(data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['updateDate'],data['url']))
        # elif e.args[0] != 1062:
        #     print("DB에러:",e)
        #     print("SQL:",sqlInsert,list(data.values()))
        #     print("data:",data)

    finally:
        conn.close()

# 이모티콘 삭제 처리
def remove_emoji(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE);
    return re_pattern.sub('', data)

# 좋아요수 가져오는 함수
def getSearchLike(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT like_cnt FROM facebook_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 댓글수 가져오는 함수
def getSearchReply(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT reply_cnt FROM facebook_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 조회수 가져오는 함수
def getSearchView(url,conn,curs):
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')

    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT view_cnt FROM facebook_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 서브제목 가져오는 함수
def getSubcontents(url,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT sns_subcontent FROM facebook_videos where url = %s order by createDate limit 1;"
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = ''
            # print(a)
            return a

# 페이스북 날짜 처리 함수
def settingDate(abbr):
    date = abbr['title']
    time = None;vdate = None;ztime = None
    if date.find("년") != -1:
        arrDate = date.split(" ")
        vdate = arrDate[0].replace("년","-")+arrDate[1].replace("월","-")+arrDate[2].replace("일","")
        ztime = arrDate[4]
        time = arrDate[5].split(":")[0]
        min = arrDate[5].split(":")[1]
    elif date.find("-") != -1:
        arrDate = date.split(" ")
        vdate = arrDate[0]
        ztime = arrDate[1]
        time = arrDate[2].split(":")[1]
        min = arrDate[2].split(":")[0]
    elif date.find(".") != -1:
        date = date.replace('.', '')
        arrDate = date.split(" ")
        vdate = '20'+arrDate[0]+'-'+arrDate[1]+'-'+arrDate[2]
        ztime = arrDate[3]
        time = arrDate[4].split(":")[0]
        min = arrDate[4].split(":")[1]
    returnDate = None
    
    if time[0] == '12':
        time[0] = '00'

    if ztime == '오전':
        returnDate = vdate+" "+time+":"+min+":00"
    elif ztime == '오후':
        returnDate = vdate+" "+str(int(time[0])+12)+":"+min+":00"

    return returnDate

# 서브제목 가져오는 함수
def getSubcontents(url,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT sns_subcontent FROM facebook_videos where url = %s order by createDate limit 1;"
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = ''
            # print(a)
            return a

# 등록날짜 가져오는 함수
def getCreateDate(url,create1,create2,conn,curs):
    check = False

    with conn.cursor() as curs:
        sql = "SELECT sns_name FROM facebook_videos where url = %s and createDate >= %s and createDate <= %s;"
        curs.execute(sql, (url,create1,create2))
        result = curs.fetchone()
        # print('접속')
        if result != None:
            check = True
            return check
        else:
            return check

# if __name__ == '__main__':
#     conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
#     curs = conn.cursor(pymysql.cursors.DictCursor)
#     print(getSearchKey(conn,curs))
#     conn.close()
