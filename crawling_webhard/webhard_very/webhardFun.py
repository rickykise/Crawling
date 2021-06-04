import re

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'acc_very_list'
        data = {
            'ACC_OSP_ID': args[0],
            'ACC_Cnt_Num': args[1],
            'ACC_User_ID': args[2],
            'ACC_Buy_Date': args[3],
            'ACC_Cnt_ID': args[4],
            'ACC_Seller': args[5],
            'ACC_Cnt_Title': args[6],
            'ACC_pay': args[7],
            'ACC_Admin_Date': args[8],
            'ACC_Admin_State': args[9]
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

# acc_very_osp 가져오는 함수
def getKeyword(osp_id,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = "SELECT ACC_Osp_ID, ACC_User_ID, ACC_User_PW, ACC_Keyword FROM site.acc_very_osp where ACC_Osp_ID = %s;"
        curs.execute(sql, (osp_id))
        result = curs.fetchall()

        returnValue = []
        for i in range(len(result)):
            returnValue.append(result[i][0])
            returnValue.append(result[i][1])
            returnValue.append(result[i][2])
            returnValue.append(result[i][3])

        return returnValue

# acc_very_admin 가져오는 함수
def getAdmin(osp_id,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = "SELECT ACC_Admin_ID, ACC_Admin_PW FROM site.acc_very_admin where ACC_OSP_ID = %s;"
        curs.execute(sql, (osp_id))
        result = curs.fetchall()

        returnValue = []
        for i in range(len(result)):
            returnValue.append(result[i][0])
            returnValue.append(result[i][1])

        return returnValue
