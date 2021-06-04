import re

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'community_data'
        data = {
            'community_name': args[0],
            'community_title': args[1],
            'community_content': args[2],
            'community_writer': args[3],
            'community_writer_IP': args[4],
            'writeDate': args[5],
            'title_key': args[6],
            'keyword': args[7],
            'keyword_type': args[8],
            'url': args[9],
            'board_number': args[10],
            'createDate': now,
            'updateDate':now
        }

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql, list(data.values()))
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

# 이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

# 이모티콘 삭제 처리 2
def remove_emoji2(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE)

    return re_pattern.sub('', data)

# db에 넣을 keyword setting
def getPutKeyword(title,text,arr):
    key = {
        'find':0,
        'keyword':''
    }
    for item in arr:
        findnum = title.find(item.replace("영화",""))
        if key['keyword'] == '' and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})
        if key['keyword'] != '' and key['find'] >= int(findnum) and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})

    if key['keyword'] == '':
        for item in arr:
            findnum = text.find(item.replace("영화",""))
            if key['keyword'] == '' and int(findnum) != -1:
                key.update({'find':findnum,'keyword':item})
            if key['keyword'] != '' and key['find'] >= int(findnum) and int(findnum) != -1:
                key.update({'find':findnum,'keyword':item})

    return key['keyword']

# db에 넣을 keyword_type get
def getPutKeywordType(keyword,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword_type FROM keyword_data WHERE keyword = %s;'
        curs.execute(sql, (keyword))
        kType = curs.fetchone()
        if kType:
            result = kType[0]
    return result

# 내용 키워드 체크
def checkKeyword(title,text,add,delete,keyword=None):
    textResult = False
    titleResult = False

    if title:
        if any(title.find(s.replace("영화","")) != -1 for s in add):
            if all(title.find(s) == -1 for s in delete):
                titleResult = True
            else:
                titleResult = False
        else:
            titleResult = False
    if text:
        if any(text.find(s.replace("영화","")) != -1 for s in add):
            if all(text.find(s) == -1 for s in delete):
                textResult = True
            else:
                textResult = False
        else:
            textResult = False

    returnVal = textResult or titleResult
    if keyword:
        returnVal = textResult and titleResult

    return returnVal

# 제외,포함검색어 가져오는 함수
def getKeyword(prop,kmain,idx,conn,curs):
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
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where keyword_property=%s  and user_idx = 9;'
        curs.execute(sql, ('포함'))
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][0]:{'add':[],'del':[]}})
        returnValue[result[i][0]]['add'] = getKeyword('포함',result[i][0],result[i][1],conn,curs)
        returnValue[result[i][0]]['del'] = getKeyword('제외',result[i][0],result[i][1],conn,curs)

    with conn.cursor() as curs:
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and user_idx!=%s and keyword_type!=%s and keyword is not null and user_idx != 21;"
        curs.execute(sql,('포함','9',''))
        result = curs.fetchall()

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
