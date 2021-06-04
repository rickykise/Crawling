import re
import pymysql
import datetime

# 이모티콘 삭제 처리
def remove_emoji(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE);
    return re_pattern.sub('', data)

# 내용 키워드 체크
def checkKeyword(text,add,delete):
    result = False

    if any(text.find(s.replace("영화","")) != -1 for s in add):
        if all(text.find(s) == -1 for s in delete):
            result = True
        else:
            result = False
    else:
        result = False

    return result

# db에 널을 keyword setting
def getPutKeyword(text,arr):
    key = {
        'find':0,
        'keyword':''
    }
    for item in arr:
        findnum = text.find(item.replace("영화",""))
        if key['keyword'] == '' and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})
        if key['keyword'] != '' and key['find'] >= int(findnum) and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})

    return key['keyword']

# db에 넣을 keyword_type get
def getPutKeywordType(keyword,conn,curs):
    returnVal = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword_type FROM keyword_data WHERE keyword = %s;'
        curs.execute(sql, (keyword))
        kType = curs.fetchone()
        if kType:
            returnVal = kType[0]
    return returnVal

# 제외,포함검색어 가져오는 함수
def getKeyword(prop,kmain,idx,conn,curs):
    rKeyword = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword FROM keyword_data WHERE user_idx = %s and keyword_main=%s and keyword_property = %s;'
        curs.execute(sql, (idx,kmain,prop))
        returnValue = curs.fetchall()
        rKeyword = []
        if prop == '포함':
            rKeyword.append(kmain)
        for i in range(len(returnValue)):
            rKeyword.append(str(returnValue[i]).replace("(","").replace(")","").replace(",","").replace("\'",""))
    return rKeyword

# 검색키워드 가져오는 함수
def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and user_idx!=%s and keyword_type!=%s and keyword is not null;"
        curs.execute(sql,('포함','9',''))
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][1]:{'add':[],'del':[]}})
        returnValue[result[i][1]]['add'] = getKeyword('포함',result[i][0],result[i][2],conn,curs)
        returnValue[result[i][1]]['del'] = getKeyword('제외',result[i][0],result[i][2],conn,curs)

    return returnValue

# 메인키워드 가져오는 함수
def getMainKeyword(dicKey,title):
    returnValue = None
    for item in dicKey:
        for akey in dicKey[item]['add']:
            if title.find(akey) != -1:
                returnValue = item
    return returnValue

# 등록날짜 가져오는 함수
def getCreateDate(url,create1,create2,conn,curs):
    check = False

    with conn.cursor() as curs:
        sql = "SELECT sns_name FROM facebook_videos where url = %s and createDate >= %s and createDate <= %s;"
        curs.execute(sql, (url,create1,create2))
        result = curs.fetchone()
        print('접속')
        if result != None:
            check = True
            return check
        else:
            return check

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

#페이스북 그래프
def insert4(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
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

#idc 페이스북 그래프
def insert5(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='116.120.58.60',user='soas',password='qwer1234',db='union',charset='utf8')
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

# 서브제목 가져오는 함수
def getSubcontents(url,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT sns_subcontent FROM facebook_videos where url = %s order by createDate limit 1;"
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                print('널아니얌')
                return b
        else:
            a = ''
            print('널이다!!!!')
            return a

# if __name__ == '__main__':
#     conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
#     curs = conn.cursor(pymysql.cursors.DictCursor)
#     print(getSearchKey(conn,curs))
#     conn.close()
