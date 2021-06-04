import re
import pymysql
conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

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

# 제목 제거 함수
def titleNull(title):

    title = title.replace('.', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '')

    return title

# url 가져오는 함수
def getSearchUrl():
    with conn.cursor() as curs:
        sql = "SELECT osp_id, osp_url FROM osp_o_list where osp_state = 1;"
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

# DB Info 저장하는 함수
def insertInfo(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'osp_info'
        data = {
            'osp_id': args[0],
            'osp_g_rank': args[1],
            'osp_k_rank': args[2],
            'osp_v_total': args[3],
            'osp_v_str': args[4],
            'osp_v_cNum': '0',
            'osp_i_regdate': now
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

#DB Info 삭제 함수
def dbDelete(osp_id,conn,curs):
    sql = "delete from osp_info where osp_id=%s order by osp_i_regdate asc limit 1; "
    curs.execute(sql,(osp_id))
    conn.commit()
