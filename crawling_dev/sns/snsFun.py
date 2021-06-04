import re
import pymysql

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'sns_data'
        data = {
            'sns_name': 'youtube',
            'sns_title': args[0],
            'sns_content': args[1],
            'url': args[2],
            'title_key': args[3],
            'keyword': args[4],
            'writeDate': args[5],
            'sns_writer': args[6],
            'like_cnt': args[7],
            'share_cnt': args[8],
            'reply_cnt':args[9],
            'view_cnt': args[10],
            'createDate': now,
            'updateDate': now
        }
        if data['keyword'] == '':
            data['keyword'] = data['title_key']

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        # if e.args[0] == 1062: break
        if e.args[0] == 1062:
            sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, updateDate=%s WHERE url=%s;"
            curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
            curs2.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
        else:
            result = True
            conn.rollback()
    finally:
        return result

# db에 널을 text setting
def setText(s,t):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&apos;", "'")
    s = s.replace("&amp;", "&")
    s = s.replace("<b>","")
    s = s.replace("</b>","")
    s = s.replace("\r","")

    if t == 0:
        s = (len(s) > 49) and s[:47]+"…" or s
        s = remove_emoji(s)

    return s

#이모티콘 삭제 처리
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

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
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and not user_idx in (22,23,24,25,26,27) and keyword_type!=%s and keyword is not null and user_idx != 21;"
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
# if __name__ == '__main__':
#     conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
#     curs = conn.cursor(pymysql.cursors.DictCursor)
#     print(getSearchKey(conn,curs))
#     conn.close()
