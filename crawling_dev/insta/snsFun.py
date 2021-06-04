import re
import pymysql

# 이모티콘 삭제 처리
def remove_emoji(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE);
    return re_pattern.sub('', data)

# 내용 키워드 체크
def checkKeyword(text,add,delete):
    result = False

    text = text.lower()

    print(text)
    for s in add:
        s = s.lower()
        print(s)
        if text.find(s.replace("영화","")) != -1:
            for s in delete:

                s = s.lower()
                print(s)
                if text.find(s) == -1:

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
        sql = 'SELECT keyword FROM keyword_data WHERE user_idx = %s and keyword_main=%s and keyword_state = 1 and keyword_property = %s;'
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
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and keyword_state = 1 and keyword_type!=%s and user_idx != 21 and keyword is not null order by createDate desc;"
        curs.execute(sql,('포함',''))
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

#sns 서버
def insert2(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='localhost',user='root',password='qwer1234',db='union',charset='utf8')
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
    if data['url'].find('/videos/') != -1:
        data['view_cnt'] = getLookup(data['url'])
    # print(data)

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

#idc 서버
def insert3(pageName,*args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = pymysql.connect(host='116.120.58.60',user='root',password='qwer1234',db='union',charset='utf8')
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
    if data['url'].find('/videos/') != -1:
        data['view_cnt'] = getLookup(data['url'])
    # print(data)

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


def updateIdx(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT url, sns_idx FROM `union`.sns_data where sns_name = 'instagram' and like_cnt >= '1000' and writeDate >= '2020-07-01 12:58:13' order by like_cnt desc;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0]
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})
        # print(returnValue)

        return returnValue

# cnt_f_list DB 업데이트 함수
def dbUpdateIdx(like, comment, idx):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "update `union`.sns_data set like_cnt=%s, reply_cnt=%s where sns_idx=%s;"
    curs.execute(sql,(like,comment,idx))
    conn.commit()

if __name__ == '__main__':
    conn = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    print(getSearchKey(conn,curs))
    conn.close()
