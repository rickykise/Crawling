import re

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
            'cnt_url': args[3],
            'cnt_price': args[4],
            'cnt_writer': args[5],
            'cnt_vol': args[6],
            'cnt_fname': args[7],
            'cnt_regdate':now,
            'cnt_chk': args[8] 
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
