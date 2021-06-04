# 네이트 톡톡 검색
import datetime,pymysql,time
import urllib.request
import requests
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from bs4 import BeautifulSoup

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
            'portal_content': args[3],
            'deviceType': 1,
            'writer': args[4],
            'writeDate': args[5],
            'title_key': args[6],
            'keyword': args[7],
            'keyword_type': args[8],
            'url': args[9],
            'createDate': now,
            'updateDate':now
        }
        if data['title_key'] == '':
            del data['title_key']

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
        sql = 'SELECT DISTINCT keyword_main,user_idx FROM keyword_data where keyword_property=%s and user_idx = 9;'
        curs.execute(sql, ('포함'))
        result = curs.fetchall()

    returnValue = {}
    for i in range(len(result)):
        returnValue.update({result[i][0]:{'add':[],'del':[]}})
        returnValue[result[i][0]]['add'] = getKeyword('포함',result[i][0],result[i][1],conn,curs)
        returnValue[result[i][0]]['del'] = getKeyword('제외',result[i][0],result[i][1],conn,curs)

    with conn.cursor() as curs:
        sql = "SELECT keyword_main,keyword,user_idx FROM keyword_data where keyword_property=%s and user_idx!=%s and keyword_type!=%s and keyword is not null;"
        curs.execute(sql,('포함','9',''))
        result = curs.fetchall()

    for i in range(len(result)):
        returnValue.update({result[i][1]:{'add':[],'del':[]}})
        returnValue[result[i][1]]['add'] = getKeyword('포함',result[i][0],result[i][2],conn,curs)
        returnValue[result[i][1]]['del'] = getKeyword('제외',result[i][0],result[i][2],conn,curs)

    return returnValue

# 메인키워드 가져오는 함수
def getMainKeyword(dicKey,title):
    returnValue = None
    for item in dicKey:
        for akey in dicKey[item]['add']:
            if title.find(akey) != -1:
                returnValue = item
    return returnValue

def startCrawling(key):
    print("키워드 : "+key)
    i = 0;
    link = 'http://pann.nate.com/search/talk?q='+key+'&sort=DD&page='
    check = True; paramKey = None; insertNum = 0

    try:
        while check:
            i = i+1
            textHtml = requests.get(link+str(i)).text
            soup = BeautifulSoup(textHtml, 'html.parser')
            ul = soup.find("ul","s_list").find_all("li")

            for item in ul:
                title = item.find('dt').find('a')['title']
                writer = item.find('dd','info').find_all('span')[1].find('a').text
                dateCheck = item.find('dd','info').find_all('span')[2].text
                writeDate = datetime.datetime.strptime(dateCheck, "%y.%m.%d %H:%M").strftime('%Y-%m-%d %H:%M:%M')
                url = item.find('dt').find('a')['href']
                html = requests.get(url).text
                tags = BeautifulSoup(html,'html.parser')
                content = tags.find('div', id='contentArea').text.replace("\n","").replace("\t","").replace("\xa0", "")
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                result = False;addKey = None
                mkey = getMainKeyword(dbKey,title)

                if mkey:
                    paramKey = None
                    addKey = dbKey[mkey]['add']
                    if mkey == '공유' or mkey == '정유미': paramKey = mkey
                    result = checkKeyword(title,None,dbKey[mkey]['add'],dbKey[mkey]['del'],paramKey)
                if result is False: break
                data = {
                    'portal_type' : 'talktalk',
                    'portal_name' : 'nate',
                    'portal_title': title,
                    'portal_content' : content,
                    'writer': writer,
                    'writeDate': writeDate,
                    'url':url,
                    'createDate': now,
                    'updateDate':now
                }
                # print(data)
                if data['writeDate'] < datetime.date.today().strftime("%Y-%m-%d"): check=False;break
                conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(data['portal_title'],data['portal_content'],addKey)
                    putKeyType = getPutKeywordType(putKey,conn,curs)
                    dbResult = insert(conn,data['portal_type'],data['portal_name'],data['portal_title'],data['portal_content'],data['writer'],data['writeDate'],dbKey[key]['add'][0],putKey,putKeyType,data['url'])
                    if dbResult:
                        return False
                finally:
                    conn.close()
            return True
    except:
        pass
    print("insert :",insertNum)
    print("============================")

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='overware.iptime.org',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("nate 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '블랙팬서':
        #     startCrawling(k)
        startCrawling(k)
    print("nate 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
