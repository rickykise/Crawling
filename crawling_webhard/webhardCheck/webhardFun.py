import re
import pymysql,time,datetime
conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
#insertall
def insertALL(data):
    connOto = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',port=3306,charset='utf8')
    try:
        curs = connOto.cursor(pymysql.cursors.DictCursor)
        print(data)
        dbResult = insert(connOto,data['Cnt_osp'],data['Cnt_url'],data['Cnt_chk'])
    except Exception as e:
        print(e)
        pass
    finally :
        connOto.close()
        return True

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'cnt_webhard'
        data = {
            'cnt_osp': args[0],
            'cnt_url': args[1],
            'cnt_regdate':now,
            'cnt_chk': args[2]
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


# 키워드 가져오는 함수
def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT k_title FROM site.k_word where k_mcp in ('sbs','kbs','jtbc') order by k_mcp desc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a
