import re
import pymysql,time,datetime
conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    connOto = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',port=3306,charset='utf8')
    connBack = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    try:
        curs = connOto.cursor(pymysql.cursors.DictCursor)
        curs2 = connBack.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(connOto,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
        insert(connBack,data['Cnt_num'],data['Cnt_osp'],data['Cnt_title'],data['Cnt_title_null'],data['Cnt_url'],data['Cnt_price'],data['Cnt_writer'],data['Cnt_vol'],data['Cnt_fname'],data['Cnt_chk'])
    except Exception as e:
        print(e)
        pass
    finally :
        connOto.close()
        connBack.close()
        return True

#insert
def insertDB(cnt_osp,cnt_title,title_null,cnt_url):
    connOto = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',port=3306,charset='utf8')
    connBack = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    try:
        curs = connOto.cursor(pymysql.cursors.DictCursor)
        curs2 = connBack.cursor(pymysql.cursors.DictCursor)
        dbResult = insert2(connOto,cnt_osp,cnt_title,title_null,cnt_url)
        insert2(connBack,cnt_osp,cnt_title,title_null,cnt_url)
    except Exception as e:
        print(e)
        pass
    finally :
        connOto.close()
        connBack.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'cnt_all'
        data = {
            'cnt_num': args[0],
            'cnt_osp': args[1],
            'cnt_title': args[2],
            'cnt_title_null': args[3],
            'cnt_url': args[4],
            'cnt_price': args[5],
            'cnt_writer': args[6],
            'cnt_vol': args[7],
            'cnt_fname': args[8],
            'cnt_regdate':now,
            'cnt_chk': args[9]
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

# DB_backup 저장하는 함수
def insert2(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'cnt_backup'
        data = {
            'cnt_osp': args[0],
            'cnt_title': args[1],
            'cnt_title_null': args[2],
            'cnt_url': args[3],
            'cnt_regdate': now
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

    title = title.replace('.', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('_', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('�', '').replace('★', '').replace('◈', '').replace('━', '').replace('【', '').replace('】', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '')

    return title


# # 체크키워드 가져오는 함수
# def getKeyword():
#     # conn.query("set character_set_results=utf8;")
#     result = None
#     with conn.cursor() as curs:
#         sql = "SELECT k_title FROM k_word where k_state = 1 and k_key = 1;"
#         curs.execute(sql)
#         result = curs.fetchall()
#
#         returnValue = {}
#         for i in range(len(result)):
#             key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '')
#             if key in returnValue:
#                 returnValue[key].append(result[i][1])
#             else:
#                 returnValue.update({key:[result[i][1]]})
#         # print(returnValue)
#
#         return returnValue


# 체크키워드 가져오는 함수
# def getKeyword():
#     sbsconn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
#     sbscurs = sbsconn.cursor(pymysql.cursors.DictCursor)
#     with sbsconn.cursor() as sbscurs:
#         sql = "SELECT k_title FROM sbs.k_word where k_nat = 'kr';"
#         sbscurs.execute(sql)
#         result = sbscurs.fetchall()
#         a = [i[0] for i in result]
#         # print(a)
#         return a

# kbs, under 체크키워드 가져오는 함수
def getKeyword():
    sbsconn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    sbscurs = sbsconn.cursor(pymysql.cursors.DictCursor)
    with sbsconn.cursor() as sbscurs:
        sql = "SELECT k_title, k_cnt_id FROM k_word where k_state = 1 and k_key = 1 and k_nat = 'kr';"
        sbscurs.execute(sql)
        result = sbscurs.fetchall()

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
def checkTitle(title, keyword, cnt_id):
    returnValue = {
        'm' : None
    }
    a = 0

    title = title.replace(' ', '')
    keyword = keyword.replace(' ', '')
    if title.find(keyword) != -1 :
        returnValue['m'] = keyword
        getDelKey = getDel(cnt_id)
        if getDelKey == []:
            returnValue['m'] = keyword
        else:
            for d in getDelKey:
                d = d.replace(' ', '')
                if title.find(d) != -1:
                    a = a+1

    if a != 0:
        returnValue['m'] = None
    return returnValue

# 제외 검색어 가져오는 함수
def getDel(delKey):
    with conn.cursor() as curs:
        sql = "SELECT k_title FROM k_word where k_key = 0 and k_L_id = %s;"
        # sql = "SELECT k_title FROM k_word where k_mcp in ('kbs', 'under') and k_key = 0 and k_L_id = %s;"
        curs.execute(sql,(delKey))
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a


#키워드 체크
def checkTitle2(title, keyword):
    returnValue = {
        'm' : None
    }

    for s in keyword.keys():
        tab = s.count(' ')
        if tab == 1:
            keyValue = []
            for i in range(tab+1):
                a = s.split(' ')[i]
                keyValue.append(a)
            if title.find(keyValue[0]) != -1 and title.find(keyValue[1]) != -1:
                returnValue['m'] = s
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
                        returnValue['m'] = s
                elif len(keyValue[1]) == 1 and len(keyValue[2]) == 1:
                    s = s.replace(' ', '')
                    if title.find(s) != -1 :
                        returnValue['m'] = s
                elif len(keyValue[0]) == 1 or len(keyValue[1]) == 1:
                    b = keyValue[0]+keyValue[1]
                    keyResultValue.append(b)
                    c = keyValue[2]
                    keyResultValue.append(c)
                    if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                        returnValue['m'] = s
                elif len(keyValue[2]) == 1:
                    b = keyValue[0]
                    keyResultValue.append(b)
                    c = keyValue[1]+keyValue[2]
                    keyResultValue.append(c)
                    if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                        returnValue['m'] = s
                else:
                    keyValue[0] = keyValue[0].replace(' ', '')
                    keyValue[1] = keyValue[1].replace(' ', '')
                    if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                        returnValue['m'] = s
            else:
                if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                    returnValue['m'] = s
        else:
            s = s.replace(' ', '')
            if title.find(s) != -1 :
                returnValue['m'] = s

    return returnValue
