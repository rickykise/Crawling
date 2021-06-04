import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

def similarwebUpdate(data):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        sql = 'update osp_similarweb set osp_state=%s, osp_nat=%s, osp_g_rank=%s, osp_c_rank=%s, osp_v_total=%s, osp_v_str=%s, osp_traffic=%s, osp_regdate=%s where osp_url=%s;'
        curs.execute(sql,(data['osp_state'],data['osp_nat'],data['osp_g_rank'],data['osp_c_rank'],data['osp_v_total'],data['osp_v_str'],data['osp_traffic'],data['osp_regdate'],data['osp_url']))
        conn.commit()
    finally:
        conn.close()

def similarwebInsert(data):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        dbResult = similarInsert(conn,data['osp_id'],data['osp_url'],data['osp_nat'],data['osp_s_nat'],data['osp_isp'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def similarInsert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'osp_similarweb'
        data = {
            'osp_id': args[0],
            'osp_url': args[1],
            'osp_nat': args[2],
            'osp_s_nat': args[3],
            'osp_isp': args[4],
            'osp_regdate': now
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

# url 가져오는 함수
def getOspTR():
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT osp_url FROM osp_similarweb where osp_state = '1' order by n_idx asc;"
            curs.execute(sql)
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a

# 제목 제거 함수
def change_Nat(osp_nat):
    nat = osp_nat
    if nat == 'Vietnam':
        nat = 'VN,Vietnam'
    elif nat == 'United States':
        nat = 'US,United States'
    elif nat == 'Turkey':
        nat = 'TR,Turkey'
    elif nat == 'Indonesia':
        nat = 'ID,Indonesia'
    elif nat == 'South Korea':
        nat = 'KR,South Korea'
    elif nat == 'China':
        nat = 'CN,China'
    elif nat == 'Philippines':
        nat = 'PH,Philippines'
    elif nat == 'Thailand':
        nat = 'TH,Thailand'
    elif nat == 'France':
        nat = 'FR,France'
    elif nat == 'France':
        nat = 'FR,France'
    elif nat == 'Russia':
        nat = 'RU,Russia'
    else:
        nat = 'default,other'

    return nat

# url 중복확인
def countNumget(now, url):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT count(*) FROM osp_similarweb where osp_regdate>=%s and osp_url=%s;"
            curs.execute(sql,(now, url))
            (number_of_rows,) = curs.fetchone()
            a = number_of_rows
            # print(a)
        finally:
            conn.close()
            return a

import requests,re
from bs4 import BeautifulSoup
# html 검사
def check_url(osp_url):
    checkText = ['drama', 'movie', 'vod', 'iptv', 'streaming']
    result = False

    r = requests.get(osp_url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    text = str(soup)

    for s in checkText:
        if text.find(s) != -1 :
            result = True

        return result
