import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert2(conn,data['Live_num'],data['Live_kor_title'],data['Live_poster'],data['Live_txt'],data['Live_search_key'],data['Live_genre'],data['Live_runtime'],data['Live_rating'],data['Live_url'],data['Live_price'],data['Live_category'],data['Live_state'],data['Live_start_date'],data['Live_end_date'],data['Live_crawling'])
    except Exception as e:
        # print(e)
        pass
    finally :
        # conn.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        tableName = 'Cnt_Live'
        data = {
            'Live_num': args[0],
            'Cp_id': 'unionc',
            'Live_kor_title': args[1],
            'Live_poster': args[2],
            'Live_txt': args[3],
            'Live_search_key': args[4],
            'Live_genre': args[5],
            'Live_runtime': args[6],
            'Live_rating': args[7],
            'Live_url': args[8],
            'Live_price': args[9],
            'Live_category': args[10],
            'Live_state' : args[11],
            'Live_start_date' : args[12],
            'Live_end_date' : args[13],
            'Live_crawling': args[14]
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


# 등급 체크 함수
def getRating(rating_check):
    Live_rating = ""
    if rating_check.find('개월') != -1:
        Live_rating = rating_check.replace('만', '').split('개월')[0].strip()+'9'
    elif rating_check.find('세') != -1:
        Live_rating = rating_check.replace('만', '').split('세')[0].strip()
    elif rating_check.find('전체관람가') != -1:
        Live_rating = 0
    elif rating_check.find('미취학') != -1:
        Live_rating = 1
    elif rating_check.find('초등학생') != -1:
        Live_rating = 8
    elif rating_check.find('중학생') != -1:
        Live_rating = 14
    elif rating_check.find('고등학생') != -1:
        Live_rating = 17
    else:
        Live_rating = None

    return Live_rating


# DB 저장하는 함수
def insert2(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        tableName = 'Cnt_Live'
        data = {
            'Live_num': args[0],
            'Cp_id': 'unionc',
            'Live_kor_title': args[1],
            'Live_poster': args[2],
            'Live_txt': args[3],
            'Live_search_key': args[4],
            'Live_genre': args[5],
            'Live_runtime': args[6],
            'Live_rating': args[7],
            'Live_url': args[8],
            'Live_price': args[9],
            'Live_category': args[10],
            'Live_state' : args[11],
            'Live_start_date' : args[12],
            'Live_end_date' : args[13],
            'Live_crawling': args[14]
        }

        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        curs.execute(sql, list(data.values()))
        conn.commit()
    except Exception as e:
        # print(e)
        if e.args[0] == 1062:
            # print('진입')
            # sql = "UPDATE Cnt_Live SET Live_start_date=%s, Live_end_date=%s WHERE Live_url=%s;"
            # curs.execute(sql,(data['Live_start_date'],data['Live_end_date'],data['Live_url']))
            sql = "UPDATE Cnt_Live SET Live_rating=%s WHERE Live_url=%s;"
            curs.execute(sql,(data['Live_rating'],data['Live_url']))
            conn.commit()
        else:
            pass
    finally:
        conn.close()

# DB 업데이트 함수
def dbUpdate(Live_txt, Live_url):
    sql = "UPDATE Cnt_Live SET Live_txt=%s WHERE Live_url=%s;"
    curs.execute(sql,(Live_txt, Live_url))
    conn.commit()

# 정보 가져오는 함수
def getLive():
    result = None
    conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT Live_url, Live_crawling FROM Cnt_Live where Live_start_date is null and live_url != '';"
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
        finally:
            conn.close()
            return returnValue


# 검색어 체크키워드 가져오는 함수
def getUrl(Live_crawling):
    conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT Live_url FROM livv.Cnt_Live where Live_crawling=%s order by Live_date desc;"
            curs.execute(sql,(Live_crawling))
            result = curs.fetchall()
            a = [i[0] for i in result]
        finally:
            conn.close()
            return a

# 검색어 체크키워드 가져오는 함수
def getTextUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT Live_idx, Live_txt FROM livv.Cnt_Live where Live_txt like '%content prdStat%' order by Live_idx desc;"
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
        finally:
            conn.close()
            return returnValue

# DB 업데이트 함수
def dbTextUpdate(Live_txt, idx):
    sql = "UPDATE Cnt_Live SET Live_txt=%s WHERE Live_idx=%s;"
    curs.execute(sql,(Live_txt, idx))
    conn.commit()
