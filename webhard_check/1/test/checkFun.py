import pymysql
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='sms@unionc',db='otogreen',port=3306,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#DB 업데이트 함수
def dbUpdate(checkNum,cnt_chk,url):
    sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
    curs.execute(sql,(cnt_chk,url))
    conn.commit()

    # print('업데이트 시작')
    # conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='sms@unionc',db='otogreen',port=3306,charset='utf8')
    # try:
    #     curs = conn.cursor(pymysql.cursors.DictCursor)
    #     sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
    #     curs.execute(sql,(cnt_chk,url))
    # finally:
    #     conn.close()
    # print('업데이트 끝')

# url 가져오는 함수
def getSearchUrl(cnt_osp):
    with conn.cursor() as curs:
        sql = "select cnt_url, cnt_chk_2 from cnt_f_detail where (cnt_osp = '"+cnt_osp+"' and cnt_chk_1 = 0 and cnt_chk_2 is null) or (cnt_osp = '"+cnt_osp+"' and cnt_chk_1 = 0 and cnt_chk_2 = 0 and cnt_chk_3 is null) order by n_idx desc ;"
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

# cnt_date 가져오는 함수
def getCntDate(url,checkNum):
    result = None
    with conn.cursor() as curs:
        sql = "SELECT cnt_date_"+checkNum+" FROM cnt_f_detail where cnt_url = %s;"
        curs.execute(sql, (url))
        nTkey = curs.fetchone()
        # print(nIdx)
        if nTkey:
            result = nTkey[0]
    return result
