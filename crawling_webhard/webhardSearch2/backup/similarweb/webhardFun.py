import re
import pymysql
conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

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
