import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['glo_num'],data['glo_site'],data['glo_nation'],data['glo_cp'],data['glo_k_word'],data['glo_title'],data['glo_title_null'],data['glo_url'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'glo_all'
        data = {
            'glo_num': args[0],
            'glo_site': args[1],
            'glo_nation': args[2],
            'glo_cp': args[3],
            'glo_k_word': args[4],
            'glo_title': args[5],
            'glo_title_null': args[6],
            'glo_url': args[7]
        }

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
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

# 제목 제거 함수
def titleNull(title):

    title = title.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '')

    return title

# 체크키워드 가져오는 함수
def getKeyword():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        sql = "SELECT keyword_main, keyword FROM keyword_data where user_idx = 33 and keyword_property = '포함';"
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

#키워드 체크
def checkTitle(title, keyword):
    returnValue = {
        'm' : None
    }
    a = 0

    for s, p in keyword.items():
        for k in p:
            k = k.replace(' ', '')
            if title.find(k) != -1 :
                returnValue['m'] = s
                getDelKey = getDel(s)
                if getDelKey == []:
                    returnValue['m'] = s
                else:
                    for d in getDelKey:
                        if title.find(d) != -1:
                            a = a+1
    if a != 0:
        returnValue['m'] = None
    return returnValue

# 제외 검색어 가져오는 함수
def getDel(keyword_main):
    with conn.cursor() as curs:
        sql = "select keyword from keyword_data where user_idx = 33 and keyword_main = %s and keyword_property = '제외';"
        curs.execute(sql,(keyword_main))
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a


#키워드 체크
def checkTitle2(title, keyword):
    returnValue = {
        'm' : None
    }

    for k, p in keyword.items():
        for s in p:
            tab = s.count(' ')
            if tab == 1:
                keyValue = []
                for i in range(tab+1):
                    a = s.split(' ')[i]
                    keyValue.append(a)
                if title.find(keyValue[0]) != -1 and title.find(keyValue[1]) != -1:
                    returnValue['m'] = k
            elif tab == 2:
                keyValue = []
                for i in range(tab+1):
                    a = s.split(' ')[i]
                    if a == '':
                        continue
                    keyValue.append(a)

                keyResultValue = []
                if len(keyValue) == 3:
                    if len(keyValue[0]) > 1 and len(keyValue[1]) > 1 and len(keyValue[2]) > 1:
                        s = s.replace(' ', '')
                        if title.find(s) != -1 :
                            returnValue['m'] = k
                    elif len(keyValue[1]) == 1 and len(keyValue[2]) == 1:
                        s = s.replace(' ', '')
                        if title.find(s) != -1 :
                            returnValue['m'] = k
                    elif len(keyValue[0]) == 1 or len(keyValue[1]) == 1:
                        b = keyValue[0]+keyValue[1]
                        keyResultValue.append(b)
                        c = keyValue[2]
                        keyResultValue.append(c)
                        if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                            returnValue['m'] = k
                    elif len(keyValue[2]) == 1:
                        b = keyValue[0]
                        keyResultValue.append(b)
                        c = keyValue[1]+keyValue[2]
                        keyResultValue.append(c)
                        if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                            returnValue['m'] = k
                    else:
                        keyValue[0] = keyValue[0].replace(' ', '')
                        keyValue[1] = keyValue[1].replace(' ', '')
                        if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                            returnValue['m'] = k
                else:
                    if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                        returnValue['m'] = k
            else:
                s = s.replace(' ', '')
                if title.find(s) != -1 :
                    returnValue['m'] = k

    return returnValue
