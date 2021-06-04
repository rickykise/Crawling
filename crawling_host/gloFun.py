import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    if data['cnt_writer'] == '':
        data['cnt_writer'] = None
    if data['host_cnt'] == '':
        data['host_cnt'] = '1'

    try:
        if data['site_p_img'] == None:
            data['site_p_img'] = None
            data['site_r_img'] = None
            data['site_img_chk'] = None
    except:
        data['site_p_img'] = None
        data['site_r_img'] = None
        data['site_img_chk'] = None

    try:
        if data['origin_url'] == None:
            data['origin_url'] = None
            data['origin_osp'] = None
    except:
        data['origin_url'] = None
        data['origin_osp'] = None

    try:
        if data['cnt_cate'] == None:
            data['cnt_cate'] = None
    except:
        data['cnt_cate'] = None

    if data['cnt_keyword'] == '':
        data['cnt_keyword'] = '1'

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insert(conn,data['cnt_id'],data['cnt_osp'],data['cnt_title'],data['cnt_title_null'],data['host_url'],data['host_cnt'],data['site_url'],data['cnt_cp_id'],data['cnt_keyword'],data['cnt_nat'],data['cnt_writer'],data['cnt_cate'],data['origin_url'],data['origin_osp'],data['site_p_img'],data['site_r_img'],data['site_img_chk'])
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
        tableName = 'cnt_f_list'
        data = {
            'cnt_id': args[0],
            'cnt_osp': args[1],
            'cnt_title': args[2],
            'cnt_title_null': args[3],
            'host_url': args[4],
            'host_cnt': args[5],
            'site_url': args[6],
            'cnt_cp_id': args[7],
            'cnt_keyword': args[8],
            'cnt_nat': args[9],
            'cnt_regdate': now,
            'cnt_regdate2': None,
            'cnt_chk': '0',
            'cnt_f_chk': '0',
            'cnt_writer': args[10],
            'cnt_cate': args[11],
            'cnt_img_chk': '0',
            'origin_url': args[12],
            'origin_osp': args[13],
            'site_p_img': args[14],
            'site_r_img': args[15],
            'site_img_chk': args[16]
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
    title = title.replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace('NEXT', '').replace(",","").replace("'", '').replace('"', '').replace('mp4', '').replace('avi', '').replace('mkv', '').replace('!', '').replace('ㅡ', '').replace('─', '').replace("+","").replace('?', '').replace('720p', '').replace('1080p', '').replace(' ', '').replace('_', '').replace('~', '').replace('–', '').replace('/', '').replace(':', '').replace('★', '')

    return title

import urllib.parse
# 검색어 체크키워드 가져오는 함수
def gethost(osp_id):
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT site_url, cnt_id, cnt_osp, cnt_title, cnt_nat FROM cnt_host_list where cnt_chk = 0 and cnt_osp=%s order by cnt_regdate desc;"
            curs.execute(sql,(osp_id))
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                # url = urllib.parse.unquote(result[i][0])
                # key = url
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                    returnValue[key].append(result[i][2])
                    returnValue[key].append(result[i][3])
                    returnValue[key].append(result[i][4])
                else:
                    returnValue.update({key:[result[i][1],result[i][2],result[i][3],result[i][4]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

# db에 널을 text setting
def setText(s,t):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&apos;", "'")
    s = s.replace("&amp;", "&")
    s = s.replace("<b>","")
    s = s.replace("</b>","")
    s = s.replace("\r","")

    if t == 0:
        s = (len(s) > 49) and s[:47]+"…" or s
        s = remove_emoji(s)

    return s

#이모티콘 삭제 처리
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

# osp 체크
def ospCheck(osp_id):
    with conn.cursor() as curs:
        sql = "SELECT osp_del FROM osp_list where osp_id=%s;"
        curs.execute(sql,(osp_id))
        result = curs.fetchall()
        a = [i[0] for i in result]
        try:
            b = a[0]
        except:
            b = None

        # print(a)
        return b

# cnt_host_list DB 업데이트 함수
def dbUpdate(url):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update cnt_host_list set cnt_chk=1 where site_url=%s;"
    curs.execute(sql,(url))
    conn.commit()

# 검색어 체크키워드 가져오는 함수
def getKeyword():
    result = None
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT k_title, k_cnt_id, n_idx, k_nat FROM k_word where k_state = 1 and k_key = 1 and k_nat is not null order by k_regdate desc;"
            curs.execute(sql)
            result = curs.fetchall()

            returnValue = {}
            for i in range(len(result)):
                key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '')
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                    returnValue[key].append(result[i][2])
                    returnValue[key].append(result[i][3])
                else:
                    returnValue.update({key:[result[i][1],result[i][2],result[i][3]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

# 제목 필터링 함수
def checkTitle(title, keyword):
    returnValue = {
        'm' : None,
        'i' : None,
        'k' : None
    }
    a = 0

    for s, p in keyword.items():
        title = title.replace(' ', '').lower()
        s = s.replace(' ', '').lower()

        if title.find(s) != -1 :
            returnValue['m'] = s
            returnValue['i'] = p[0]
            returnValue['k'] = p[1]
            getDelKey = getDel(p[0])
            if getDelKey == []:
                returnValue['m'] = s
                returnValue['i'] = p[0]
                returnValue['k'] = p[1]
            else:
                for d in getDelKey:
                    d = d.replace(' ', '').replace('-', '').lower()
                    if title.find(d) != -1:
                        a = a+1
            if a != 0:
                returnValue['m'] = None

            return returnValue
    return returnValue

# 제외 검색어 가져오는 함수
def getDel(delKey):
    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT k_title FROM k_word where k_key = 0 and k_cnt_id = %s;"
            curs.execute(sql,(delKey))
            result = curs.fetchall()
            a = [i[0] for i in result]
            # print(a)
        finally:
            conn.close()
            return a
