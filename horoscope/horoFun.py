import re
import pymysql,time,datetime

#insertall
def insertALL(data):
    conn = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='horoscope',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['horoscope_cons'],data['horoscope_cate'],data['horoscope_love'],data['horoscope_date'],data['horoscope_content'],data['writeDate'])
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
        tableName = 'horoscope'
        data = {
            'horoscope_cons': args[0],
            'horoscope_cate': args[1],
            'horoscope_love': args[2],
            'horoscope_date': args[3],
            'horoscope_content': args[4],
            'writeDate': args[5],
            'regdate': now,
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

def dateFormat(month):
    if month == "Jan":
        month = '01'
    elif month == "Feb":
        month = '02'
    elif month == "Mar":
        month = '03'
    elif month == "Apr":
        month = '04'
    elif month == "May":
        month = '05'
    elif month == "Jun":
        month = '06'
    elif month == "Jul":
        month = '07'
    elif month == "Aug":
        month = '08'
    elif month == "Sep":
        month = '09'
    elif month == "Oct":
        month = '10'
    elif month == "Nov":
        month = '11'
    elif month == "Dec":
        month = '12'
    if month == "January":
        month = '01'
    elif month == "February":
        month = '02'
    elif month == "March":
        month = '03'
    elif month == "April":
        month = '04'
    elif month == "May":
        month = '05'
    elif month == "June":
        month = '06'
    elif month == "July":
        month = '07'
    elif month == "August":
        month = '08'
    elif month == "September":
        month = '09'
    elif month == "October":
        month = '10'
    elif month == "November":
        month = '11'
    elif month == "December":
        month = '12'

    return month
