import pymysql,time,datetime
# youtube check test
def getGoogleDel():
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "select host_url, cnt_id from ((SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'china' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'france' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'indonesia' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500) UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'myanmar' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500) UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'philippines' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'russia' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500) UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'southkorea' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500) UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'thailand' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'unitedstates' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'vietnam' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where google_chk = 0 and cnt_nat = 'other' and cnt_chk in ('1','4','5','6') order by cnt_regdate desc limit 500)) x  order by cnt_nat asc;"
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
        finally:
            conn.close()
            return returnValue

# hash 가져오는 함수
def getCheckKey():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT cnt_id FROM otogreen.cnt_l_list where cnt_hash != '';"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a

def checkId(cnt_id, check_id):
    returnValue = {
        'm' : None
    }
    for s in check_id:
        sLen = len(s)
        idLen = len(cnt_id)
        if sLen != idLen:
            continue
        if cnt_id.find(s) != -1 :
            returnValue['m'] = s

    return returnValue

def googleDelUpdate(chk_num, url):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "update sbs.cnt_f_list set  google_chk=%s where host_url=%s;"
        curs.execute(sql,(chk_num,url))
        conn.commit()
    finally:
        conn.close()

# --------------- 재검수 ----------------------------

# youtube check test
def getGoogleDelRe():
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        sql = "select host_url from ((SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'china' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'france' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'indonesia' and google_chk = '1' order by cnt_regdate desc limit 500) UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'myanmar' and google_chk = '1' order by cnt_regdate desc limit 500) UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'philippines' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL (SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'russia' and google_chk = '1' order by cnt_regdate desc limit 500) UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'southkorea' and google_chk = '1' order by cnt_regdate desc limit 500) UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'thailand' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'unitedstates' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'vietnam' and google_chk = '1' order by cnt_regdate desc limit 500)UNION ALL(SELECT host_url, cnt_regdate, cnt_nat, cnt_id FROM sbs.cnt_f_list where cnt_nat = 'other' and google_chk = '1' order by cnt_regdate desc limit 500)) x  order by cnt_nat asc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def googleDelUpdateRe(chk_num, url):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = "update sbs.cnt_f_list set google_chk=%s where host_url=%s;"
        curs.execute(sql,(chk_num,url))
        conn.commit()
    finally:
        conn.close()
