# url 중복확인
def countNumget(url):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT count(*) FROM community_data where url=%s;"
            curs.execute(sql,(url))
            (number_of_rows,) = curs.fetchone()
            a = number_of_rows
            # print(a)
        finally:
            conn.close()
            return a




countNum = countNumget(now, osp_url)
if countNum >= 1:
    continue
