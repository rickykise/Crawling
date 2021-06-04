import re
import pymysql,time,datetime
conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

#insertall
def insertALL(data):
    # if data['cnt_num'] == '':
    #     data['cnt_num'] = None
    # if data['cnt_host'] == '':
    #     data['cnt_host'] = None
    if data['cnt_writer'] == '':
        data['cnt_writer'] = None
    if data['host_cnt'] == '':
        data['host_cnt'] = '1'
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
        dbResult = insert(conn,data['cnt_id'],data['cnt_osp'],data['cnt_title'],data['cnt_title_null'],data['host_url'],data['host_cnt'],data['site_url'],data['cnt_cp_id'],data['cnt_keyword'],data['cnt_nat'],data['cnt_writer'],data['cnt_cate'],data['origin_url'],data['origin_osp'])
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
        tableName = 'cnt_f_list_test'
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
            'origin_osp': args[13]
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

#insertall
def insertALLKey(data):
    if data['cnt_writer'] == '':
        data['cnt_writer'] = None
    if data['host_cnt'] == '':
        data['host_cnt'] = '1'

    conn = pymysql.connect(host='49.247.5.160',user='otogreen',password='uni1004!@',db='sbs',charset='utf8')
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbResult = insertKey(conn,data['cnt_id'],data['cnt_osp'],data['cnt_title'],data['cnt_title_null'],data['host_url'],data['host_cnt'],data['site_url'],data['cnt_cp_id'],data['cnt_keyword'],data['cnt_nat'],data['cnt_writer'],data['origin_url'],data['origin_osp'],data['cnt_keyword_nat'])
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
            'cnt_keyword_nat': args[13]
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

# 검색어 체크키워드 가져오는 함수
def getKeyword():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        # sql = "SELECT k_title, k_cp, cnt_price FROM cnt_keyprice where k_mcp in ((SELECT cp_mcp FROM cp_list where cp_state = 1 and cp_mcp in ('kbs', 'under'))) and k_state = 1;"
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

# osp_url 가져오는 함수
def getGoogleHostUrl():
    with conn.cursor() as curs:
        # sql = "select host_url, cnt_del_date from cnt_f_list where cnt_osp = 'google' and cnt_del_act = 1 and cnt_chk!=4;"
        sql = "select host_url, cnt_del_date from cnt_f_list where cnt_osp = 'google' order by n_idx desc;"
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

# 검색어 체크키워드 가져오는 함수
def getKeywordNat():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        # sql = "SELECT k_title, k_cp, cnt_price FROM cnt_keyprice where k_mcp in ((SELECT cp_mcp FROM cp_list where cp_state = 1 and cp_mcp in ('kbs', 'under'))) and k_state = 1;"
        sql = "SELECT k_title, k_cnt_id, n_idx, k_nat FROM k_word where k_state = 1 and k_key = 1 and k_nat is not null and k_nat != 'KR';"
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

def checkTitle(title, keyword):
    returnValue = {
        'm' : None,
        'i' : None,
        'k' : None
    }
    a = 0

    for s, p in keyword.items():
        title = title.replace(' ', '')
        s = s.replace(' ', '')
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
                    d = d.replace(' ', '')
                    if title.find(d) != -1:
                        a = a+1
    if a != 0:
        returnValue['m'] = None
    return returnValue

def checkTitleTest(title, cnt_id):
    returnValue = {
        'm' : None
    }
    a = 0
    returnValue['m'] = cnt_id
    getDelKey = getDel(cnt_id)
    print(getDelKey)
    if getDelKey == []:
        returnValue['m'] = cnt_id
    else:
        for d in getDelKey:
            d = d.replace(' ', '')
            if title.find(d) != -1:
                print(d)
                a = a+1


    if a != 0:
        returnValue['m'] = None
    return returnValue

# 체크키워드 가져오는 함수
# def getKeyword():
#     result = None
#     with conn.cursor() as curs:
#         sql = "SELECT k_title, k_cnt_id FROM k_word where k_state = 1 and k_key = 1;"
#         curs.execute(sql)
#         result = curs.fetchall()
#
#         returnValue = {}
#         for i in range(len(result)):
#             key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '').replace('~', '').replace('–', '').replace('/', '')
#             if key in returnValue:
#                 returnValue[key].append(result[i][1])
#             else:
#                 returnValue.update({key:[result[i][1]]})
#         # print(returnValue)
#
#         return returnValue

# 키워드 체크
# def checkTitle(title, keyword):
#     returnValue = {
#         'm' : None
#     }
#     a = 0
#
#     for s, p in keyword.items():
#         title = title.replace(' ', '')
#         s = s.replace(' ', '')
#         if title.find(s) != -1 :
#             returnValue['m'] = s
#             getDelKey = getDel(p[0])
#             if getDelKey == []:
#                 returnValue['m'] = s
#             else:
#                 for d in getDelKey:
#                     if title.find(d) != -1:
#                         a = a+1
#     if a != 0:
#         returnValue['m'] = None
#     return returnValue

# 제외 검색어 가져오는 함수
def getDel(delKey):
    with conn.cursor() as curs:
        sql = "SELECT k_title FROM k_word where k_key = 0 and k_cnt_id = %s;"
        curs.execute(sql,(delKey))
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# 키워드 체크2
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

# osp_url 가져오는 함수
# def getHostUrl(cnt_osp):
#     with conn.cursor() as curs:
#         sql = "select host_url, cnt_del_date from cnt_f_list where cnt_del_act=1 and cnt_chk!=4 and cnt_osp=%s;"
#         curs.execute(sql,(cnt_osp))
#         result = curs.fetchall()
#
#         returnValue = {}
#         for i in range(len(result)):
#             key = result[i][0]
#             if key in returnValue:
#                 returnValue[key].append(result[i][1])
#             else:
#                 returnValue.update({key:[result[i][1]]})
#         # print(returnValue)
#
#         return returnValue

# youkuosp_url 가져오는 함수
def getYoukuHostUrl():
    with conn.cursor() as curs:
        sql = "select host_url, cnt_del_date from cnt_f_list where cnt_osp = 'youku' and cnt_del_act = 1 and cnt_chk!=4;"
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


# osp_url 가져오는 함수
def getHostUrl():
    with conn.cursor() as curs:
        sql = "select host_url, cnt_del_date from cnt_f_list where cnt_del_act = 1 and cnt_chk!=4;"
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


# site_url 가져오는 함수
def getOspUrl():
    result = None
    with conn.cursor() as curs:
        sql = "select osp_url, osp_id from osp_list order by n_idx asc;"
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

# cnt_f_list DB 업데이트 함수
def dbUpdate(checkNum,now,host_url):
    if checkNum == 1:
        sql = "update cnt_f_list set cnt_chk=4, cnt_regdate2=%s, cnt_dend_act=1, cnt_dend_date=%s where host_url=%s;"
        curs.execute(sql,(now,now,host_url))
        conn.commit()
    else:
        sql = "update cnt_f_list set cnt_regdate2=%s where host_url=%s;"
        curs.execute(sql,(now,host_url))
        conn.commit()

# osp_list DB 업데이트 함수
def ospUpdate(del_date,osp_id):
    sql = "update osp_list set osp_del = 1, osp_del_date=%s where osp_id=%s;  "
    curs.execute(sql,(del_date,osp_id))
    conn.commit()

# osp_list DB 업데이트 함수
def ospUpdateback(osp_id):
    sql = "update osp_list set osp_del = 0 where osp_id=%s;  "
    curs.execute(sql,(osp_id))
    conn.commit()

# 구글 체크url 가져오는 함수
def getUrl():
    with conn.cursor() as curs:
        sql = "SELECT cnt_url FROM url_check;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def checkUrl(url, getUrl):
    returnValue = {
        'm' : None
    }

    for u in getUrl:
        if url.find(u) != -1 :
            returnValue['m'] = u

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
        print(getDelKey)
        if getDelKey == []:
            returnValue = keyword
        else:
            for d in getDelKey:
                d = d.replace(' ', '')
                if title.find(d) != -1:
                    print(d)
                    a = a+1
        if a != 0:
            returnValue = ''

        return returnValue


# 검색어 체크키워드 가져오는 함수
def getKeywordNaver():
    with conn.cursor() as curs:
        sql = "SELECT k_title, k_cnt_id, n_idx FROM k_word where k_state = 1 and k_key = 1 group by k_cnt_id;"
        curs.execute(sql)
        result = curs.fetchall()

        returnValue = {}
        for i in range(len(result)):
            key = result[i][0].replace("\ufeff","").replace('?','').replace('!','').replace(',','').replace('-','').replace('&','').replace('.','').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace('-', '').replace("'", '').replace('"', '').replace('ㅡ', '').replace("+","").replace("-","").replace("_","").replace(' ', '')
            if key in returnValue:
                returnValue[key].append(result[i][1])
                returnValue[key].append(result[i][2])
            else:
                returnValue.update({key:[result[i][1],result[i][2]]})
        # print(returnValue)

        return returnValue

import urllib.request
import json,re
# 네이버 search api
def searchNAPI(category,keyword,display,start,sort):
    client_id = "XVudreaGdyXDSiYrhqpG"
    client_secret = "txULvjQq4d"
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/"+category+".json?query="+encText+"&display="+display+"&start="+start+"&sort="+sort # json 결과
    try:
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
    except Exception as e:
        print("Error Code:",e)

    return False

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

# 구글 체크url 가져오는 함수
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

# 검색어 체크키워드 가져오는 함수
def getKeywordCH():
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        sql = "SELECT k_title, k_cnt_id, n_idx, k_nat FROM k_word where k_state = 1 and k_key = 1 and k_nat in ('us', 'cn');"
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

# 검색어 체크키워드 가져오는 함수
def getKeywordDaily():
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

# daily check test
def getdailytest():
    with conn.cursor() as curs:
        sql = "SELECT host_url FROM sbs.cnt_f_list where cnt_osp = 'dailymotion' order by cnt_regdate desc;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# youtube check test
def getyoutubetest():
    with conn.cursor() as curs:
        sql = "SELECT cnt_url FROM sbs.youtube_check;"
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

# cnt_f_list DB 업데이트 함수
def dbYoutubeUpdate(cnt_writer,url):
    sql = "update youtube_check set cnt_writer=%s where cnt_url=%s;"
    curs.execute(sql,(cnt_writer,url))
    conn.commit()

import numpy as np
import cv2
from matplotlib import pyplot as plt
def url_to_image(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)

    return image

def imgCheck(url1, url2):
    # url = 'http://61.82.113.196:8181/poster/poster.jpg'
    img1 = url_to_image(url1)
    img2 = url_to_image(url2)

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(matches))]

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.3*n.distance:
            matchesMask[i]=[1,0]

    check_text = matchesMask.count([1,0])

    # draw_params = dict(matchColor = (0,255,0),singlePointColor = (255,0,0),matchesMask = matchesMask,flags = 2)
    # knn_image = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
    # plt.imshow(knn_image)
    # plt.show()

    return check_text
