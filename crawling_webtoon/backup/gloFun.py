import re
import pymysql,time,datetime

#insertall
def insertALL(data):
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
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

# 제목 제거 함수
def titleNull(title):
    title = title.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '').replace('_', '').replace('~', '').replace('–', '').replace('/', '').replace(':', '').replace('★', '').replace('.', '')

    return title

# 검색어 체크키워드 가져오는 함수
def getTitle():
    result = None
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT cnt_title, cnt_title_eng, cnt_cp_id, cnt_id FROM webtoon.cnt_list;"
            curs.execute(sql)
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '').replace(':', '')
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
        s = s.replace(' ', '').lower()
        if title.find(s) != -1 :
            returnValue['m'] = s
            returnValue['i'] = p[1]
            returnValue['k'] = p[2]
        else:
            if title.find(p[0]) != -1 :
                returnValue['m'] = p[0]
                returnValue['i'] = p[1]
                returnValue['k'] = p[2]

    return returnValue

#insertall
def insertKeep(data):
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insertK(conn,data['craw_osp_id'],data['craw_domain'],data['craw_cp_id'],data['craw_cnt_id'],data['craw_title'],data['craw_site_url'],data['craw_url'],data['craw_title_num'])
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
            'craw_site_url': args[5],
            'craw_url': args[6],
            'craw_title_num': args[7],
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
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT * FROM webtoon.craw_all group by craw_site_url order by craw_date desc limit 100;"
            # sql = "SELECT * FROM webtoon.craw_all where craw_state = '0' order by craw_date desc;"
            curs.execute(sql)
            result = curs.fetchall()
        finally:
            conn.close()
            return result

# cnt_f_list DB 업데이트 함수
def dbUpdate(cp_id,cnt_id,craw_idx):
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update craw_all set craw_cp_id=%s, craw_cnt_id=%s, craw_state='1' where craw_idx=%s;"
    curs.execute(sql,(cp_id,cnt_id,craw_idx))
    conn.commit()

# cnt_f_list DB 업데이트 함수
def dbNullUpdate(craw_idx):
    conn = pymysql.connect(host='211.193.58.218',user='webtoon',password='admin2006!@',db='webtoon',port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update craw_all set craw_state='1' where craw_idx=%s;"
    curs.execute(sql,(craw_idx))
    conn.commit()
