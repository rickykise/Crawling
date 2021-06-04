import pymysql
conn = pymysql.connect(host='61.82.113.197',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)
conn2 = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='otogreen',port=3306,charset='utf8')
curs2 = conn.cursor(pymysql.cursors.DictCursor)

# url 가져오는 함수
def getSearchUrl(cnt_osp):
    with conn.cursor() as curs:
        # sql = "select cnt_url, cnt_chk_2 from cnt_f_detail where (cnt_osp = '"+cnt_osp+"' and cnt_chk_1 = 0 and cnt_chk_2 is null) or (cnt_osp = '"+cnt_osp+"' and cnt_chk_1 = 0 and cnt_chk_2 = 0 and cnt_chk_3 is null) order by n_idx desc ;"
        sql = 'select cnt_url, cnt_chk_2 from cnt_f_detail where (cnt_chk_1 = 0 and cnt_chk_2 is null or cnt_chk_1 = 0 and cnt_chk_2 = 0 and cnt_chk_3 is null) order by n_idx desc Limit 50;'
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

#DB 업데이트 함수
def dbUpdate(checkNum,cnt_chk,url):
    sql = "UPDATE cnt_f_detail SET cnt_chk_"+checkNum+"=%s WHERE cnt_url=%s;"
    curs.execute(sql,(cnt_chk,url))
    curs2.execute(sql,(cnt_chk,url))
    conn.commit()
    conn2.commit()

# 제목 제거 함수
def titleNull(title):

    title = title.replace('.', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('_', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('�', '').replace('★', '').replace('◈', '').replace('━', '').replace('【', '').replace('】', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '')

    return title

# kbs, under 체크키워드 가져오는 함수
def getKeyword():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        # sql = "SELECT k_title, k_cp, cnt_price FROM cnt_keyprice where k_mcp in ((SELECT cp_mcp FROM cp_list where cp_state = 1 and cp_mcp in ('kbs', 'under'))) and k_state = 1;"
        sql = "SELECT k_title, k_cp, cnt_price FROM cnt_keyprice where k_mcp in ('kbs', 'under') and k_state = 1;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '')
            if key in returnValue:
                returnValue[key].append(result[i][1],result[i][2])
            else:
                returnValue.update({key:[result[i][1],result[i][2]]})
        # print(returnValue)

        return returnValue

#키워드 체크
def checkTitle(title, keyword):
    returnValue = {
        'm' : None,
        'p' : None
    }

    for s, p in keyword.items():
        s = s.replace(' ', '')
        if title.find(s) != -1 :
            returnValue['m'] = s
            returnValue['p'] = p[1]

    return returnValue
