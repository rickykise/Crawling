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
            'cnt_title_null': args[3],
            'cnt_url': args[4],
            'cnt_price': args[5],
            'cnt_writer': args[6],
            'cnt_vol': args[7],
            'cnt_fname': args[8],
            'cnt_regdate':now,
            'cnt_chk': args[9]
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

# 제목 제거 함수
def titleNull(title):

    title = title.replace('.', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '')

    return title

# 키워드 가져오는 함수
def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT k_title FROM site.k_word where k_mcp in ('sbs','kbs','jtbc') order by k_mcp desc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# pdpop url 가져오는 함수
def getSearchUrl2(conn,curs):
    with conn.cursor() as curs:
        sql = "select STRAIGHT_JOIN a.cnt_url, a.cnt_f_regdate from (select STRAIGHT_JOIN f.n_idx, f.cnt_L_idx, f.cnt_L_id, f.cnt_num, f.cnt_osp, f.cnt_title as title, f.cnt_url, f.cnt_price, f.cnt_writer, f.cnt_vol, f.cnt_cate, f.cnt_fname, f.cnt_mcp, f.cnt_cp, f.cnt_keyword, f.cnt_f_regdate,SUBSTRING_INDEX(d.cnt_img_1, '/', 2) AS path, d.cnt_img_1,d.cnt_img_2,d.cnt_img_3, DATE_FORMAT(d.cnt_date_1, '%Y-%m-%d %H:%i:%s') AS cnt_date_1, DATE_FORMAT(d.cnt_date_2, '%Y-%m-%d %H:%i:%s') AS cnt_date_2, DATE_FORMAT(d.cnt_date_3, '%Y-%m-%d %H:%i:%s') AS cnt_date_3, d.cnt_chk_1,d.cnt_chk_2,d.cnt_chk_3 from cnt_f_list as f join cnt_f_detail as d ON  d.f_idx = f.n_idx where f.cnt_f_regdate between '2019-01-08 23:31:45' and '2019-01-24  23:59:59'  and f.cnt_mcp = 'jtbc' and (f.cnt_osp in (select osp_id from osp_o_list where osp_tstate = 1)) and f.cnt_osp='pdpop' order by f.cnt_f_regdate asc ) as a left join osp_o_list as o on a.cnt_osp = o.osp_id left join k_word as k on a.cnt_keyword = k.n_idx left join cnt_l_list as c on a.cnt_L_idx = c.n_idx order by a.cnt_f_regdate asc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# pdpop url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = "SELECT cnt_url FROM cnt_all where cnt_osp = 'pdpop' and cnt_regdate <= '2019-01-23 13:00:00' order by CHAR_LENGTH(cnt_price) desc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# 체크키워드 가져오는 함수
def getKeyword(conn,curs):
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        sql = "SELECT k_title, k_cp FROM site.k_word where k_mcp in ('sbs','kbs','jtbc', 'under');"
        curs.execute(sql)
        result = curs.fetchall()


        returnValue = {}
        for i in range(len(result)):
            key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '')
            if key in returnValue:
                returnValue[key].append(result[i][1])
            else:
                returnValue.update({key:[result[i][1]]})
        # print(returnValue)

        return returnValue

#키워드 체크
def checkTitle(title, keyword):
    returnValue = {
        'm' : None
    }

    for s in keyword.keys():
        s = s.replace(' ', '')
        if title.find(s) != -1 :
            returnValue['m'] = s

    return returnValue

#키워드 체크
def checkTitle2(title, keyword):
    returnValue = {
        'm' : None
    }

    for s in keyword.keys():
        tab = s.count(' ')
        if tab == 1:
            keyValue = []
            for i in range(tab+1):
                a = s.split(' ')[i]
                keyValue.append(a)
            if title.find(keyValue[0]) != -1 and title.find(keyValue[1]) != -1:
                returnValue['m'] = s
        elif tab == 2:
            keyValue = []
            for i in range(tab+1):
                a = s.split(' ')[i]
                if a == '':
                    continue
                keyValue.append(a)

            keyResultValue = []
            if len(keyValue) == 3:
                if len(keyValue[0]) > 1 and len(keyValue[1]) > 1 and len(keyValue[2]) > 1:
                    s = s.replace(' ', '')
                    if title.find(s) != -1 :
                        returnValue['m'] = s
                elif len(keyValue[1]) == 1 and len(keyValue[2]) == 1:
                    s = s.replace(' ', '')
                    if title.find(s) != -1 :
                        returnValue['m'] = s
                elif len(keyValue[0]) == 1 or len(keyValue[1]) == 1:
                    b = keyValue[0]+keyValue[1]
                    keyResultValue.append(b)
                    c = keyValue[2]
                    keyResultValue.append(c)
                    if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                        returnValue['m'] = s
                elif len(keyValue[2]) == 1:
                    b = keyValue[0]
                    keyResultValue.append(b)
                    c = keyValue[1]+keyValue[2]
                    keyResultValue.append(c)
                    if title.find(keyResultValue[0]) != -1 or title.find(keyResultValue[1]) != -1:
                        returnValue['m'] = s
                else:
                    keyValue[0] = keyValue[0].replace(' ', '')
                    keyValue[1] = keyValue[1].replace(' ', '')
                    if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                        returnValue['m'] = s
            else:
                if title.find(keyValue[0]) != -1 or title.find(keyValue[1]) != -1:
                    returnValue['m'] = s
        else:
            s = s.replace(' ', '')
            if title.find(s) != -1 :
                returnValue['m'] = s

    return returnValue
