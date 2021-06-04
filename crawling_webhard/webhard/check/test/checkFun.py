# url 가져오는 함수
def getSearchUrl(cnt_osp,checkNum,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT cnt_url FROM cnt_f_detail where cnt_osp = '"+cnt_osp+"' and cnt_chk_"+checkNum+" is null;"
        # print('sql1:', sql)
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# url2 가져오는 함수
def getSearchUrl2(cnt_osp,checkNum,conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT cnt_url FROM cnt_f_detail where cnt_osp = '"+cnt_osp+"' and cnt_chk_2 is not null and cnt_chk_"+checkNum+" is null;"
        # print('sql1:', sql)
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# cnt_date 가져오는 함수
def getCntDate(url,checkNum,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = "SELECT cnt_date_"+checkNum+" FROM cnt_f_detail where cnt_url = %s;"
        # print('sql2:', sql)
        curs.execute(sql, (url))
        nTkey = curs.fetchone()
        # print(nIdx)
        if nTkey:
            result = nTkey[0]
    return result
