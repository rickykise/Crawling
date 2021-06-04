import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALLKey(data):
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


    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insertKey(conn,data['cnt_id'],data['cnt_osp'],data['cnt_title'],data['cnt_title_null'],data['host_url'],data['host_cnt'],data['site_url'],data['cnt_cp_id'],data['cnt_keyword'],data['cnt_nat'],data['cnt_writer'],data['origin_url'],data['origin_osp'],data['site_p_img'],data['site_r_img'],data['cnt_keyword_nat'])
    except Exception as e:
        print(e)
        pass
    finally :
        conn.close()
        return True

# DB 저장하는 함수
def insertKey(conn,*args):
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
            'cnt_img_chk': '0',
            'origin_url': args[11],
            'origin_osp': args[12],
            'site_p_img': args[13],
            'site_r_img': args[14],
            'cnt_keyword_nat': args[15]
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

#이모티콘 삭제 처리
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

# 검색어 체크키워드 가져오는 함수
def getKeywordYoutube():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        sql = "SELECT k_title, k_cnt_id, n_idx, k_nat FROM k_word where k_state = 1 and k_key = 1 and k_nat is not null;"
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

        return returnValue

# 유튜브 글쓴이 가져오는 함수
def getWriter():
    with conn.cursor() as curs:
        sql = "SELECT cnt_writer FROM youtube_check;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def checkWriter(cnt_writer, writerGet):
    returnValue = {
        'm' : None
    }

    for u in writerGet:
        if cnt_writer.find(u) != -1 :
            returnValue['m'] = u

    return returnValue

def googleCheckTitle(title, keyword, id):
    returnValue = ''
    a = 0
    title = title.replace(' ', '')
    keyword = keyword.replace(' ', '')

    if title.find(keyword) != -1 :
        returnValue = keyword
        getDelKey = getDel(id)
        if getDelKey == []:
            returnValue = keyword
        else:
            for d in getDelKey:
                d = d.replace(' ', '')
                if title.find(d) != -1:
                    a = a+1
        if a != 0:
            returnValue = ''

        return returnValue

# 제외 검색어 가져오는 함수
def getDel(delKey):
    with conn.cursor() as curs:
        sql = "SELECT k_title FROM k_word where k_key = 0 and k_cnt_id = %s;"
        curs.execute(sql,(delKey))
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a
