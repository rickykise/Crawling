import os
import sys
import urllib.request
import json,re

# 네이버 search api
def searchNAPI(category,keyword,display,start,sort):
    client_id = "rKPa0Ubq8anIE1p_IDAg"
    client_secret = "AuyDMRd17F"
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

# 다음 search api
def searchDAPI(category,keyword,page):
    apikey = "KakaoAK 5ffc76bc940c42ccf03bf109f49c793f"
    encText = urllib.parse.quote(keyword)
    url = "https://dapi.kakao.com/v2/search/"+category+"?query="+encText+"&page="+page+"&size=50&sort=recency" # json 결과

    request = urllib.request.Request(url)
    request.add_header("Authorization",apikey)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        json.loads(response_body.decode('utf-8'))
        return json.loads(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)

    return False

# 네이버 api - url 줄임
def shortURL(shortUrl):
    client_id = "rKPa0Ubq8anIE1p_IDAg"
    client_secret = "AuyDMRd17F"
    encText = urllib.parse.quote(shortUrl)
    data = "url=" + encText
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        rUrl = json.loads(response_body.decode('utf-8'))['result']
        return rUrl['url']
    else:
        print("Error Code:" + rescode)
    return shortUrl

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'portal_data'
        data = {
            'portal_type': args[0],
            'portal_name': args[1],
            'portal_title': args[2],
            'deviceType': 1,
            'writer': args[3],
            'writeDate': args[4],
            'title_key': args[5],
            'keyword': args[6],
            'keyword_type': args[7],
            'url': args[8],
            'createDate': now,
            'updateDate':now
        }
        if data['title_key'] == '':
            del data['title_key']

        if args[0] == 'media' or args[0] == 'reporter':
            if data['keyword_type'] == '':
                del data['keyword_type']
            if args[0] == 'reporter':
                data['reporter_name'] = args[9]
            data['media_name'] = data['portal_name']
            data['media_title'] = data['portal_title']
            data['media_content'] = args[3]
            tableName = 'media_data'
            del(data['portal_type'],data['deviceType'],data['portal_name'],data['portal_title'],data['writer'])


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

# DB 저장하는 함수
def insertCommunity(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'community_data'
        data = {
            'community_name': args[0],
            'community_title': args[1],
            'community_content': args[2],
            'community_writer': 'naver',
            'writeDate': args[3],
            'title_key': args[4],
            'keyword': args[5],
            'keyword_type': args[6],
            'url': args[7],
            'createDate': now,
            'updateDate':now
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# 이름 가져오기
def getWriter(dic,pName,pType):
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        for item in dic:
            # alert창 체크
            try:
                driver.get(item['url'])
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                print('alert창이 있어 건너뜁니다.')
                driver.quit()
                driver = webdriver.Chrome("c:\python36\driver\chromedriver")
                continue
            except:
                pass

            uWriter = None
            if pType == 'cafe':
                try:
                    if pName == 'naver':
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cafe_main")))
                        driver.switch_to.frame(element)
                        uWriter = driver.find_element(by='class name', value="p-nick").text
                    else:
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "down")))
                        driver.switch_to.frame(element)
                        uWriter = driver.find_element(by='class name', value="article_writer").find_element(by='class name', value="txt_point").text
                except Exception as e:
                    if pName == 'naver':
                        driver.switch_to_window("naver_login")
                        driver.close()
                        driver.switch_to_window("")
                    continue
            else:
                try:
                    if pName == 'naver':
                        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "mainFrame")))
                        driver.switch_to.frame(element)
                        uWriter = driver.find_element(By.CLASS_NAME, "bg-body").find_element(By.CLASS_NAME, "nick").text
                    else:
                        if url.find('daum') != -1:
                            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='ProfileMenuMain']/div/div[1]/a")))
                            uWriter = element.text
                except Exception as e:
                    continue

            if uWriter:
                import pymysql
                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                curs = conn.cursor(pymysql.cursors.DictCursor)
                try:
                    sql = "update portal_data set writer=%s where portal_type=%s and portal_name=%s and keyword=%s and url=%s;"
                    curs.execute(sql,(uWriter.strip(),pType,pName,item['keyword'],item['url']))
                    conn.commit()
                finally:
                    conn.close()
    except Exception as e:
        print('driverError:',e)
    finally:
        driver.quit()

#이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

#이모티콘 삭제 처리 2
def remove_emoji2(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE);
    return re_pattern.sub('', data)

# web url 확인
from openpyxl import load_workbook
def checkLink(url):
    delURL = []
    wb = load_workbook('../제외url.xlsx', read_only=True)
    ws = wb.get_sheet_by_name("Sheet2")
    for r in ws.rows:
        delURL.append(r[0].value)

    if any(url.find(s) != -1 for s in delURL):
        return False
    else:
        if url.find("viki") != -1:
            url = url.split("?")[0]
        elif url.find("heraldcorp") != -1:
            url = url.split("&RURL=")[0]

    return url

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

# db에 넣을 keyword setting
def getPutKeyword(title,text,arr):
    key = {
        'find':0,
        'keyword':''
    }
    for item in arr:
        findnum = title.find(item.replace("영화",""))
        if key['keyword'] == '' and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})
        if key['keyword'] != '' and key['find'] >= int(findnum) and int(findnum) != -1:
            key.update({'find':findnum,'keyword':item})

    if key['keyword'] == '' and text is not None:
        for item in arr:
            findnum = text.find(item.replace("영화",""))
            if key['keyword'] == '' and int(findnum) != -1:
                key.update({'find':findnum,'keyword':item})
            if key['keyword'] != '' and key['find'] >= int(findnum) and int(findnum) != -1:
                key.update({'find':findnum,'keyword':item})

    return key['keyword']

# db에 넣을 keyword_type get
def getPutKeywordType(keyword,conn,curs):
    returnVal = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword_type FROM keyword_data WHERE keyword = %s;'
        curs.execute(sql, (keyword))
        kType = curs.fetchone()
        if kType:
            returnVal = kType[0]
    return returnVal

# 내용 키워드 체크
def checkKeyword(title,text,add,delete,keyword=None):
    textResult = None
    titleResult = None

    if text:
        if any(text.find(s.replace("영화","")) != -1 for s in add):
            if all(text.find(s) == -1 for s in delete):
                textResult = True
            else:
                textResult = False
        else:
            textResult = False
    if title:
        if any(title.find(s.replace("영화","")) != -1 for s in add):
            if all(title.find(s) == -1 for s in delete):
                titleResult = True
            else:
                titleResult = False
        else:
            titleResult = False

    returnVal = textResult or titleResult
    if keyword:
        returnVal = textResult and titleResult

    return returnVal

# 제외,포함검색어 가져오는 함수
def getKeyword(prop,kmain,idx,conn,curs):
    rKeyword = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword FROM keyword_data WHERE user_idx = %s and keyword_main=%s and keyword_property = %s;'
        curs.execute(sql, (idx,kmain,prop))
        returnValue = curs.fetchall()
        rKeyword = []
        if prop == '포함':
            rKeyword.append(kmain)
        for i in range(len(returnValue)):
            rKeyword.append(str(returnValue[i]).replace("(","").replace(")","").replace(",","").replace("\'",""))
    return rKeyword

# 메인 키워드 가져오는 함수
def getMainKey(conn,key):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword_main FROM `union`.keyword_data where keyword=%s;'
        curs.execute(sql, key)
        result = curs.fetchone()

    return result[0]

# 검색키워드 가져오는 함수
def getSearchKey(conn,curs):
    with conn.cursor() as curs:
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where keyword_property=%s and user_idx in (22,23,24,25,26,27) and user_idx != 21;'
        curs.execute(sql, ('포함'))
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][0]:{'add':[],'del':[]}})
        returnValue[result[i][0]]['add'] = getKeyword('포함',result[i][0],result[i][1],conn,curs)
        returnValue[result[i][0]]['del'] = getKeyword('제외',result[i][0],result[i][1],conn,curs)

    with conn.cursor() as curs:
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and not user_idx in (22,23,24,25,26,27) and user_idx != 21 and keyword_type!=%s and keyword is not null;"
        curs.execute(sql,('포함',''))
        result = curs.fetchall()

    for i in range(len(result)):
        returnValue.update({result[i][1]:{'add':[],'del':[]}})
        returnValue[result[i][1]]['add'] = getKeyword('포함',result[i][0],result[i][2],conn,curs)
        returnValue[result[i][1]]['del'] = getKeyword('제외',result[i][0],result[i][2],conn,curs)

    return returnValue

if __name__ == '__main__':
    import pymysql
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getSearchKey(conn,curs)

# 포함 키워드 가져오는 함수
def getAddKeyword(conn,curs):
    rKeyword = None
    with conn.cursor() as curs:
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where keyword_property=%s and user_idx!=1'
        curs.execute(sql, ('포함'))
        result = curs.fetchall()
        rKeyword = []

        for i in result:
            sql = 'SELECT keyword FROM keyword_data WHERE user_idx = %s and keyword_property = %s;'
            curs.execute(sql, (i[1], '포함'))
            returnValue = curs.fetchall()

            for i in range(len(returnValue)):
                putKey = str(returnValue[i]).replace("(","").replace(")","").replace(",","").replace("\'","")
                if putKey not in rKeyword:
                    rKeyword.append(putKey)

    return rKeyword

# 기자 가져오는 함수
def getSearchReporter(conn,curs):
    returnValue = None
    with conn.cursor() as curs:
        sql = 'SELECT reporter_media_name,reporter_name FROM reporter_data;'
        curs.execute(sql)
        result = curs.fetchall()
        returnValue = []
        for i in range(len(result)):
            returnValue.append([result[i][0].replace(u'\ufeff', ''),result[i][1]])
    return returnValue

# 스타와치 키워드 가져오는 함수
def getStarWachKey(conn,curs):
    returnValue = None
    with conn.cursor() as curs:
        sql = 'SELECT distinct(keyword_main) FROM keyword_data where user_idx in (22,23,24,25,26,27);'
        curs.execute(sql)
        result = curs.fetchall()
    returnValue = [i[0] for i in result]
    return returnValue

# 메인키워드 가져오는 함수
def getMainKeyword(dicKey,title):
    returnValue = None
    for item in dicKey:
        for akey in dicKey[item]['add']:
            if title.find(akey) != -1:
                returnValue = item
    return returnValue

# 기자 가져오는 함수
def getReporter(conn,curs):
    # conn.query("set character_set_results=utf8;")
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT reporter_media_name,reporter_name  FROM reporter_data;'
        curs.execute(sql)
        result = curs.fetchall()


        returnValue = {}
        for i in range(len(result)):
            media = result[i][0].replace("\ufeff","")
            if media in returnValue:
                returnValue[media].append(result[i][1])
            else:
                returnValue.update({media:[result[i][1]]})
        # print(returnValue)

        return returnValue

# DB 저장하는 함수
def insertNaver(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_videos'
        data = {
            'portal_title' : args[0],
            'portal_subtitle' : args[1],
            'portal_writer' : args[2],
            'url' : args[3],
            'like_cnt' : args[4],
            'reply_cnt' : args[5],
            'share_cnt' : 0,
            'view_cnt' : args[6],
            'writeDate' : args[7],
            'board_number' : args[8],
            'createDate' : now,
            'updateDate' : now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
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

def insertNaver2(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'naver_graph'
        data = {
            'url' : args[0],
            'view_cnt' : args[1],
            'like_cnt' : args[2],
            'reply_cnt' : args[3],
            'writeDate' : args[4],
            'createDate' : now,
            'updateDate' : now
        }
        placeholders = ', '.join(['%s'] * len(data))
        columns = ', '.join(data.keys())
        sql = "INSERT INTO "+tableName+" ( %s ) VALUES ( %s );" % (columns, placeholders)
        # print(sql)
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

# 좋아요수 가져오는 함수
def getSearchLike(url,conn):
    import pymysql
    import datetime
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT like_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 댓글수 가져오는 함수
def getSearchReply(url,conn):
    import pymysql
    import datetime
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT reply_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 조회수 가져오는 함수
def getSearchView(url,conn):
    import pymysql
    import datetime
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours = 1)
    now1 = now-delta
    now2 = now-delta
    create1 = now1.strftime('%Y-%m-%d %H:00:00')
    create2 = now2.strftime('%Y-%m-%d %H:59:59')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    # print(create1)
    # print(create2)

    with conn.cursor() as curs:
        sql = "SELECT view_cnt FROM naver_videos where createDate >= "+"'"+create1 +"'"+ " and createDate <= "+"'"+create2+"'"+" and url = %s;"
        # print(sql)
        curs.execute(sql, (url))
        result = curs.fetchone()
        a = result
        if a != None:
            for b in a:
                # print(b)
                return b
        else:
            a = 0
            return a

# 등록날짜 가져오는 함수
def getCreateDate(url,create1,create2,conn):
    import pymysql
    import datetime
    check = False
    curs = conn.cursor(pymysql.cursors.DictCursor)

    with conn.cursor() as curs:
        sql = "SELECT portal_title FROM naver_videos where url = %s and createDate >= %s and createDate <= %s;"
        curs.execute(sql, (url,create1,create2))
        result = curs.fetchone()
        # print('접속')
        if result != None:
            check = True
            return check
        else:
            return check
