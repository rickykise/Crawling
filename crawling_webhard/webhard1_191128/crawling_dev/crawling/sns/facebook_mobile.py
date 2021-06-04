# 페이스북 크롤링
import re
import sys
import pymysql
import datetime,time
from snsFun import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# 페이스북 날짜 처리 함수
def getTime(date):

    dateGettime = date
    try:
        if dateGettime.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(dateGettime, "%Y년 %m월 %d일 오후 %H:%M").strftime('%Y-%m-%d %H:%M:%S')
            clock = datetime.datetime.strptime(dateGettime, "%Y년 %m월 %d일 오후 %H:%M").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        elif dateGettime.find('오전') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "%Y년 %m월 %d일 오전 %H:%M").strftime('%Y-%m-%d %H:%M:%S')
        # else:
        #     pass
    except:
        pass

    # print(writeDate)
    return writeDate

def settingDate(date):
    now = datetime.datetime.now().strftime('%Y')
    dateGettime = date

    try:
        if dateGettime.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(dateGettime, "%m월 %d일 오후 %H:%M").strftime(now+'-%m-%d %H:%M:%S')
            clock = datetime.datetime.strptime(dateGettime, "%m월 %d일 오후 %H:%M").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        elif dateGettime.find('오전') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "%m월 %d일 오전 %H:%M").strftime(now+'-%m-%d %H:%M:%S')
        # else:
        #     pass
    except:
        pass

    # print(writeDate)
    return writeDate

def getTimecheck(date):

    dateGettime = date

    if date.find('분')!= -1:
        datech = dateGettime.split("분")[0]
        datecheck = int(datech)
        now = datetime.datetime.now()
        date2 = now - datetime.timedelta(minutes=datecheck)
        writeDate = date2.strftime('%Y-%m-%d %H:%M:00')
    elif date.find('시간')!= -1:
            datech = dateGettime.split("시간")[0]
            datecheck = int(datech)
            now = datetime.datetime.now()
            date2 = now - datetime.timedelta(hours=datecheck)
            writeDate = date2.strftime('%Y-%m-%d %H:00:00')
    else:
        pass

    return writeDate

def getTodaycheck(date,day):

    if day == '오늘':
        print(day)
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        dateGettime = date.split("오늘 ")[1]
    elif day == '어제':
        print(day)
        current = datetime.datetime.now()
        yesterDay = current - datetime.timedelta(days=1)
        now = yesterDay.strftime('%Y-%m-%d')
        dateGettime = date.split("어제 ")[1]

    try:
        if dateGettime.find('오후') != -1:
            writeDatech = datetime.datetime.strptime(dateGettime, "오후 %H:%M").strftime(now + ' %H:%M:%S')
            clock = datetime.datetime.strptime(dateGettime, "오후 %H:%M").strftime('%I')
            clock2 = int(clock)+12
            cl = str(clock2)
            writeDate = datetime.datetime.strptime(writeDatech, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d '+cl+':%M:%S')
        elif dateGettime.find('오전') != -1:
            writeDate = datetime.datetime.strptime(dateGettime, "오전 %H:%M").strftime(now + ' %H:%M:%S')
        # else:
        #     pass
    except:
        pass

    # print(writeDate)
    return writeDate

# 게시물 url 확인
def searchHtml(href):
    return href and not re.compile("hc_ref=").search(href)

# 페이스북 총 게시물 크롤링
def getPageSource(key):
    print("키워드:",key)
    result = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
        driver.set_window_size(500, 1080) # 크롬 창 사이즈
        driver.get('https://m.facebook.com/graphsearch/str/'+key+'/stories-keyword/stories-public?tsid=0.8484371015225547&source=pivot&ref=content_filter')
        # 'https://www.facebook.com/hashtag/'+key+'?source=feed_text'
        time.sleep(3)

        for i in range(10):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            except:
                pass
            try:
                end = driver.find_element_by_class_name("uiScrollableAreaContent").find_element_by_id("browse_end_of_results_footer")
                if end: break
            except:
                pass
        # 페이지 html 가져와서 데이터 추출
        elm = driver.find_element_by_id("viewport").get_attribute('innerHTML')
        soup = BeautifulSoup(elm, 'html.parser')
        result = soup.find_all("div","_2h4o _1p82")

    # except TimeoutException as ex:
    #     print("**********TimeoutException*************")
    except:
        pass
    finally:
        driver.quit()

    return result

def startCrawling(key):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updateNum = 0;insertNum = 0
    all = getPageSource(key)
    if all is None: return
    for item in all:
        # print(item)
        try:
            contentsaa = item.find('div', '_5rgt').text.replace("\n","").replace("\t","").replace("\xa0", "").strip()
            contents = remove_emoji(contentsaa).replace("[]","").replace(" ","")
        except:
            print('콘텐츠 에러')
            continue
        writer = item.find('h3', '_52jd').text.strip().split("님이")[0]
        url = ''
        writeDate = ''
        try:
            if item.find('div', '_2ip_'):
                url = item.find('div', '_2ip_').find('a')['href']
                if url.find('facebook.com') == -1:
                    url = 'https://www.facebook.com'+item.find('div', '_2ip_').find('a')['href'].split("&ref")[0]
            elif item.find('a', 'touchable'):
                url = item.find('a', 'touchable')['href']
        except:
            pass

        writeD = item.find('abbr').text.strip()
        # print(writeD)
        if writeD.find('년') != -1:
            writeDate = getTime(writeD)
        elif writeD.find('분') != -1 or writeD.find('시간') != -1:
            writeDate = getTimecheck(writeD)
        elif writeD.find('오늘') != -1:
            day = '오늘'
            writeDate = getTodaycheck(writeD, day)
        elif writeD.find('어제') != -1:
            day = '어제'
            writeDate = getTodaycheck(writeD, day)
        else:
            writeDate = settingDate(writeD)

        lrs = item.find_all('span', '_28wy')
        like = 0
        reply = 0
        share = 0
        try:
            if len(lrs) == 1:
                like = item.find('span', 'like_def').text.strip().split(" ")[1].split("개")[0]
            elif len(lrs) == 2:
                like = item.find('span', 'like_def').text.strip().split(" ")[1].split("개")[0]
                reply = item.find('span', 'cmt_def').text.strip().split(" ")[1].split("개")[0]
            elif len(lrs) == 3:
                like = item.find('span', 'like_def').text.strip().split(" ")[1].split("개")[0]
                reply = item.find('span', 'cmt_def').text.strip().split(" ")[1].split("개")[0]
                share = item.find_all('span', '_28wy')[2].text.strip().split(" ")[1].split("회")[0]
        except:
            pass
        contentss = item.find('div', '_5rgt').text
        putKey = getPutKeyword(contents,dbKey[key]['add'])

        # print(url)
        print(writeDate)
        print("===================")
        if url == '' or url == None:
            continue
        elif writeDate == '' or writeDate == None:
            continue
        elif writeDate.find('2018') == -1:
            # print('2018년도가 아니야!!!!')
            continue

        data = {
            'sns_name': 'facebook',
            'sns_title': writer+'#'+putKey, #제목
            'sns_content': contents, # 내용
            'url': url, # url
            'title_key': dbKey[key]['add'][0],
            'keyword': putKey, # 키워드
            'writeDate':  writeDate, # 날짜
            'sns_writer': writer, # 글쓴이
            'like_cnt': like, # 좋아요 수
            'share_cnt': share, # 공유 수
            'reply_cnt': reply, # 댓글 수
            'view_cnt': 0, # 조회 수
            'createDate': now,
            'updateDate': now
        }
        if data['keyword'] == '':
            data['keyword'] = dbKey[key]['add'][0]
        # print(data)
        if data is None: continue
        result = checkKeyword(data['sns_content'],dbKey[key]['add'],dbKey[key]['del'])
        if result:
            conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                data['sns_writer'] = (len(data['sns_writer']) > 50) and data['sns_writer'][:47]+"…" or data['sns_writer']
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
            except Exception as e:
                if e.args[0] == 1062:
                    sql = "UPDATE sns_data SET like_cnt=%s, reply_cnt=%s, share_cnt=%s, view_cnt=%s, writeDate=%s, updateDate=%s WHERE url=%s;"
                    curs.execute(sql,(data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['view_cnt'],data['writeDate'],data['updateDate'],data['url']))
                    updateNum = updateNum+1
                else:
                    pass
            else:
                insertNum = insertNum+1
            finally:
                conn.commit()
                conn.close()

    print("총 게시물:",len(all))
    print("update : ",updateNum," / insert : ",insertNum)
    print("==============================================")

if __name__=='__main__':
    conn = pymysql.connect(host='61.82.113.197',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    # print(dbKey.keys())
    conn.close()

    start_time = time.time()
    print("페이스북 크롤링 시작")
    # count = 0
    for key in dbKey.keys():
        # if dbKey[key]['add'][0] == '패키지':
        #     startCrawling(key)
        # elif dbKey[key]['add'][0] == '암수살인':
        #     startCrawling(key)
        startCrawling(key)
    print("페이스북 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
