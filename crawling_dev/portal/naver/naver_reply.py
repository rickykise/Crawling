# 네이버 댓글 검색
import datetime,pymysql,time
import sys,os
import urllib.request
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from selenium import webdriver
from bs4 import BeautifulSoup

# DB 저장하는 함수
def insert(conn,*args):
    import pymysql
    import datetime
    result = False
    try:
        curs = conn.cursor(pymysql.cursors.DictCursor)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tableName = 'reply_data'
        data = {
            'news_idx': args[0],
            'reply_comm_num': args[1],
            'reply_content': args[2],
            'reply_writer' : args[3],
            'writeDate': args[4],
            'textType': args[5],
            'title_key': args[6],
            'keyword' : args[7],
            'createDate': now,
            'updateDate':now
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

# 이모티콘 삭제 처리 1
def remove_emoji(data):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

    return emoji_pattern.sub(r'', data)

# 이모티콘 삭제 처리 2
def remove_emoji2(data):
    re_pattern = re.compile(u'[^\u0000-\uFFFF]', re.UNICODE)

    return re_pattern.sub('', data)

# idx 가져오는 함수
def getSearchIdx(url,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT news_idx FROM news_data WHERE url = %s;'
        curs.execute(sql, (url))
        nIdx = curs.fetchone()
        # print(nIdx)
        if nIdx:
            result = nIdx[0]
    return result

# title_key 가져오는 함수
def getSearchTkey(url,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT title_key FROM news_data WHERE url = %s;'
        curs.execute(sql, (url))
        nTkey = curs.fetchone()
        # print(nIdx)
        if nTkey:
            result = nTkey[0]
    return result

# keyword 가져오는 함수
def getSearchKeyword(url,conn,curs):
    result = None
    with conn.cursor() as curs:
        sql = 'SELECT keyword FROM news_data WHERE url = %s;'
        curs.execute(sql, (url))
        nkeyword = curs.fetchone()
        # print(nIdx)
        if nkeyword:
            result = nkeyword[0]
    return result

# url 가져오는 함수
def getSearchUrl(conn,curs):
    with conn.cursor() as curs:
        sql = 'SELECT url FROM news_data where news_state = 1 and news_type = "A";'
        curs.execute(sql)
        result = curs.fetchall()
        a = [i[0] for i in result]
        # print(a)
        return a

def main():
    url = 'http://entertain.naver.com/comment/list?oid=076&aid=0003229233'
    print("url:", url)
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    try:
        link= url
        driver = webdriver.Chrome("c:\python36\driver\chromedriver")
        driver.get(link)
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="cbox_module"]/div/div[6]/div[1]/div/ul/li[2]/a/span[2]').click()
        time.sleep(3)
        for i in range(0, 38) :
            try:
                driver.find_element_by_css_selector(".u_cbox_btn_more").click()
                time.sleep(3)
                i +=1
            except:
                break
        html = driver.find_element_by_class_name("u_cbox_content_wrap").get_attribute('innerHTML')
        soup = BeautifulSoup(html,'html.parser')
        ul = soup.find("ul").find_all("li")

        for item in ul:
            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Date = item.find('div', 'u_cbox_info_base').find_all('span')[0]['data-value'].split("T")[0]
            writetime = item.find('div', 'u_cbox_info_base').find_all('span')[0]['data-value'].split("T")[1]. split("+")[0]
            date = Date+' '+writetime
            writeDate = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d %H:%M:%S')
            reply_comm_num = item.find('div', 'u_cbox_info_base').find_all('span')[1].find('a')['data-param'].split(":")[1]. split(",")[0]
            writer = item.find('div', 'u_cbox_info').find('span', 'u_cbox_nick').text


            data = {
                'reply_comm_num' : reply_comm_num,
                'reply_content' : item.find('div', 'u_cbox_text_wrap').text.replace("\n","").replace("\t",""),
                'reply_writer' : writer,
                'writeDate' : writeDate,
                'textType' : '',
                'createDate': now,
                'updateDate':now
            }
            # print(data)
            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                putIdx = getSearchIdx(url,conn,curs)
                putTkey = getSearchTkey(url,conn,curs)
                getPutKeyword = getSearchKeyword(url,conn,curs)
                dbResult = insert(conn,putIdx,data['reply_comm_num'],data['reply_content'],data['reply_writer'],data['writeDate'],data['textType'],putTkey,getPutKeyword,data['createDate'],data['updateDate'])
                if dbResult:
                    return False
            finally :
                conn.close()

    finally:
        driver.close()
    return True
    print("url:", url)

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getUrl = getSearchUrl(conn,curs)
    conn.close()

    print("NEWS 댓글 크롤링 시작")
    for u in getUrl:
        main()
    print("NEWS 댓글 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
