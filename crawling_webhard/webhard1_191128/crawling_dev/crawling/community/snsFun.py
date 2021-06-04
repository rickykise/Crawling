import re
import pymysql

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
# if __name__ == '__main__':
#     conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
#     curs = conn.cursor(pymysql.cursors.DictCursor)
#     print(getSearchKey(conn,curs))
#     conn.close()
