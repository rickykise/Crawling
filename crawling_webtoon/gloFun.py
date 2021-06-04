import re
import pymysql,time,datetime

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['craw_osp_id'],data['craw_domain'],data['craw_title'],data['craw_site_url'],data['craw_url'],data['craw_title_num'])
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
        tableName = 'craw_all'
        data = {
            'craw_osp_id': args[0],
            'craw_domain': args[1],
            'craw_title': args[2],
            'craw_site_url': args[3],
            'craw_url': args[4],
            'craw_title_num': args[5],
            'craw_date': now
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
    title = title.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '').replace('_', '').replace('~', '').replace('–', '').replace('/', '').replace(':', '').replace('★', '').replace('.', '')

    return title

# 검색어 체크키워드 가져오는 함수
def getTitle():
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT cnt_title, cnt_title_eng, cnt_cp_id, cnt_id FROM webtoon.cnt_list;"
            curs.execute(sql)
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                    returnValue[key].append(result[i][2])
                    returnValue[key].append(result[i][3])
                else:
                    returnValue.update({key:[result[i][1],result[i][2],result[i][3]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

def checkTitle(title, keyword):
    returnValue = {
        'm' : None,
        'i' : None,
        'k' : None
    }
    for s, p in keyword.items():
        title = title.replace(' ', '').lower()
        st = s.replace(' ', '').lower()
        if title.find(st) != -1 :
            returnValue['m'] = s
            returnValue['i'] = p[1]
            returnValue['k'] = p[2]
        else:
            if p[0] != '':
                if title.find(p[0]) != -1 :
                    returnValue['m'] = p[0]
                    returnValue['i'] = p[1]
                    returnValue['k'] = p[2]

    return returnValue

# --------------------글자수 체크 추가---------------------------
# def checkTitle(title, keyword):
#     returnValue = {
#         'm' : None,
#         'i' : None,
#         'k' : None
#     }
#     for s, p in keyword.items():
#         title = title.replace(' ', '').lower()
#         st = s.replace(' ', '').lower()
#         if title.find(st) != -1 :
#             checkResult =  checkLen(title, s)
#             if checkResult == True:
#                 returnValue['m'] = s
#                 returnValue['i'] = p[1]
#                 returnValue['k'] = p[2]
#         else:
#             if p[0] != '':
#                 if title.find(p[0]) != -1 :
#                     checkResult =  checkLen(title, p[0])
#                     if checkResult == True:
#                         returnValue['m'] = p[0]
#                         returnValue['i'] = p[1]
#                         returnValue['k'] = p[2]
#
#     return returnValue
#
# def checkLen(title, title2):
#     check1 = len(titleNull(title))
#     check2 = len(titleNull(title2))
#
#     if check1 != check2:
#         return False
#     else:
#         return True
# ------------------------------------------------------------

#insertall
def insertKeep(data):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insertK(conn,data['craw_osp_id'],data['craw_domain'],data['craw_cp_id'],data['craw_cnt_id'],data['craw_title'],data['craw_title_null'],data['craw_site_url'],data['craw_url'],data['craw_title_num'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insertK(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'craw_keep'
        data = {
            'craw_osp_id': args[0],
            'craw_domain': args[1],
            'craw_cp_id':  args[2],
            'craw_cnt_id' :  args[3],
            'craw_title': args[4],
            'craw_title_null': args[5],
            'craw_site_url': args[6],
            'craw_url': args[7],
            'craw_title_num': args[8],
            'craw_date': now,
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

# 검색어 체크키워드 가져오는 함수
def getAll():
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            # sql = "SELECT * FROM webtoon.craw_all where craw_state = '0' order by craw_date desc;"
            sql = "SELECT * FROM webtoon.craw_all where craw_cp_id is null order by craw_date desc;"
            curs.execute(sql)
            result = curs.fetchall()
        finally:
            conn.close()
            return result

# cnt_f_list DB 업데이트 함수
def dbUpdate(cp_id,cnt_id,craw_idx):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update craw_all set craw_cp_id=%s, craw_cnt_id=%s, craw_state='1' where craw_idx=%s;"
    curs.execute(sql,(cp_id,cnt_id,craw_idx))
    conn.commit()

# cnt_f_list DB 업데이트 함수
def dbNullUpdate(craw_idx):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update craw_all set craw_state='1' where craw_idx=%s;"
    curs.execute(sql,(craw_idx))
    conn.commit()

# site_url 가져오는 함수
def getOspUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "select osp_url, osp_idx from osp_list where osp_state = '1' order by osp_idx asc;"
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

# site_url 가져오는 함수
def getOspVpnUrl():
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "select osp_url, osp_idx from osp_list where osp_state_vpn = '1' order by osp_idx asc;"
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
def stateUpdate(osp_state, idx):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "update osp_list set osp_state=%s, osp_del_date=%s where osp_idx=%s;"
    curs.execute(sql,(osp_state,now,idx))
    conn.commit()

# cnt_f_list DB 업데이트 함수
def stateVpnUpdate(osp_state, idx):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "update osp_list set osp_state_vpn=%s, osp_del_vpn_date=%s where osp_idx=%s;"
    curs.execute(sql,(osp_state,now,idx))
    conn.commit()

# site_url 가져오는 함수
def getGoogleKeyword():
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "select osp_title, osp_idx from osp_list order by osp_idx asc;"
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

#insertall
def insertGoogle(data):
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insertG(conn,data['google_title'],data['google_url'],data['osp_title'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insertG(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'google_list'
        data = {
            'google_title': args[0],
            'google_url': args[1],
            'osp_title': args[2],
            'google_date': now
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

# 검색어 체크키워드 가져오는 함수
def getUrl(osp_id):
    result = None
    conn = pymysql.connect(host='49.247.5.41',user='webtoon',password='admin2006!@',db='webtoon',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "select osp_url from osp_list where osp_same=%s order by osp_date desc limit 1;"
            curs.execute(sql,(osp_id))
            result = curs.fetchone()
        finally:
            conn.close()
            return result
