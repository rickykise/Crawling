import time,datetime
from datetime import date, timedelta
# cnt_date 가져오는 함수
def getCntDate(url,checkNum):
    result = None
    with conn.cursor() as curs:
        if checkNum == '3':
            sql = "SELECT cnt_date_"+checkNum+", cnt_chk_2 FROM cnt_f_detail where cnt_url = %s;"
            curs.execute(sql, (url))
            result = curs.fetchall()

            if result[0][1] == '0':
                now = date.today()
                result = now + timedelta(2)
            else:
                result = result[0][0]

            return result
        else:
            sql = "SELECT cnt_date_"+checkNum+" FROM cnt_f_detail where cnt_url = %s;"
            curs.execute(sql, (url))
            nTkey = curs.fetchone()

            if nTkey:
                result = nTkey[0]

            return result
