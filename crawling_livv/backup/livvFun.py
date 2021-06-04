import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    conn = pymysql.connect(host='49.247.5.176',user='livv',password='livv2020!@',db='livv',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['Live_num'],data['Live_kor_title'],data['Live_poster'],data['Live_search_key'],data['Live_genre'],data['Live_runtime'],data['Live_url'],data['Live_price'],data['Live_category'],data['Live_state'],data['Live_crawling'])
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
        tableName = 'Cnt_Live'
        data = {
            'Live_num': args[0],
            'Cp_id': 'unionc',
            'Live_kor_title': args[1],
            'Live_poster': args[2],
            'Live_search_key': args[3],
            'Live_genre': args[4],
            'Live_runtime': args[5],
            'Live_url': args[6],
            'Live_price': args[7],
            'Live_category': args[8],
            'Live_state' : args[9],
            'Live_crawling': args[10]
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
