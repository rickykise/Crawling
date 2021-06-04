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
def settingDate(abbr):
    date = abbr['title']
    time = None;vdate = None;ztime = None
    if date.find("년") != -1:
        arrDate = date.split(" ")
        vdate = arrDate[0].replace("년","-")+arrDate[1].replace("월","-")+arrDate[2].replace("일","")
        ztime = arrDate[4]
        time = arrDate[5].split(":")
    elif date.find("-") != -1:
        arrDate = date.split(" ")
        vdate = arrDate[0]
        ztime = arrDate[1]
        time = arrDate[2].split(":")
    returnDate = None

    if time[0] == '12':
        time[0] = '00'

    if ztime == '오전':
        returnDate = vdate+" "+time[0]+":"+time[1]
    elif ztime == '오후':
        returnDate = vdate+" "+str(int(time[0])+12)+":"+time[1]

    return returnDate

# 게시물 url 확인
def searchHtml(href):
    return href and not re.compile("hc_ref=").search(href)

# 크롤링 데이터 setting
def dataProcessing(item):
    textTag = item.find("div","_1dwg").find("div","_5pbx")
    url = None;data = None;now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if textTag:
        text = remove_emoji(textTag.text)
        try:
            urlEle = item.find("abbr").parent
            abbr = urlEle.find('abbr')
            url = (urlEle['href'].find('https://www.facebook.com') == -1) and 'https://www.facebook.com'+urlEle['href'] or urlEle['href']
            writer = item.find("span","fwb").find_all("a",limit=1)[0].text
            if writer.find("님이 게시") != -1:
                writer = writer.split("님이 게시")[0]

            data = {
                'sns_name': 'facebook',
                'sns_title': remove_emoji(writer)+"#벤츠", #제목
                'sns_content': text.replace("더 보기","").replace("...",""), # 내용
                'url': url, # url
                'title_key': '벤츠',
                'keyword' : '벤츠', # 키워드
                'writeDate':  settingDate(abbr), # 날짜
                'sns_writer': remove_emoji(writer), # 글쓴이
                'like_cnt': 0, # 좋아요 수
                'share_cnt': 0, # 공유 수
                'reply_cnt': 0, # 댓글 수
                'view_cnt': 0, # 조회 수
                'createDate': now,
                'updateDate': now
            }
        except Exception as e:
            print("===========================\n",type(e),e,"\n===========================")

        if data['writeDate']:
            # 좋아요 수 체크
            if item.find("a",{"class","_3emk"}):
                if item.find("a",{"class","_3emk"})['aria-label'].split(" ")[0] == "좋아요":
                    likeNum = item.find("a",{"class","_3emk"})['aria-label']
                    data['like_cnt'] = (likeNum != '') and int(''.join(list(filter(str.isdigit,likeNum)))) or 0
            # 댓글 수 체크
            if item.find("div",{"class","_ipo"}):
                replyShare = item.find("div",{"class","_ipo"}).get_text(' ',strip=True).split(" ")
                for i in range(len(replyShare)):
                    if replyShare[i] == "댓글":
                        replyNum = replyShare[i+1]
                        data['reply_cnt'] = (replyNum != '') and int(''.join(list(filter(str.isdigit,replyNum)))) or 0
                    elif replyShare[i] == "공유":
                        shareNum = replyShare[i+1]
                        data['share_cnt'] = (shareNum != '') and int(''.join(list(filter(str.isdigit,shareNum)))) or 0
                    elif replyShare[i] == "조회":
                        viewNum = replyShare[i+1]
                        data['view_cnt'] = int(''.join(list(filter(str.isdigit,viewNum))))
                        if viewNum.find('만') != -1:
                            if viewNum.find('.') != -1:
                                data['view_cnt'] = data['view_cnt'] * 1000
                            else:
                                data['view_cnt'] = data['view_cnt'] * 10000
    return data

# 페이스북 총 게시물 크롤링
def getPageSource():
    print("키워드 : 벤츠")
    result = None
    try:
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chrome_options)
        driver.get('https://www.facebook.com/pg/CJCGV/posts/')

        wait = WebDriverWait(driver, 10)
        emailEle = wait.until(EC.presence_of_element_located((By.NAME,'email')))
        passEle = wait.until(EC.presence_of_element_located((By.NAME,'pass')))
        emailEle.send_keys('susan1457@naver.com')
        passEle.send_keys('qustndus_dkdlel')
        btnEle = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginbutton"]')))
        btnEle.click()
        time.sleep(3)

        driver.get('https://www.facebook.com/pg/CJCGV/posts/')
        time.sleep(3)
        for i in range(3):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
            except:
                pass
        # 페이지 html 가져와서 데이터 추출
        elm = driver.find_elements_by_class_name("_1xnd")[1].get_attribute('innerHTML')
        # print(elm)
        soup = BeautifulSoup(elm, 'html.parser')
        result = soup.find_all("div",{"class","_4-u2"})
    except TimeoutException as ex:
        print("**********TimeoutException*************")
    finally:
        driver.quit()

    return result

def startCrawling():
    updateNum = 0;insertNum = 0
    all = getPageSource()
    if all is None: return
    for item in all:
        data = dataProcessing(item)
        if data is None: continue
        conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
        try:
            curs = conn.cursor(pymysql.cursors.DictCursor)
            data['sns_writer'] = (len(data['sns_writer']) > 50) and data['sns_writer'][:47]+"…" or data['sns_writer']
            placeholders = ', '.join(['%s'] * len(data))
            columns = ', '.join(data.keys())
            sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
            curs.execute(sql, list(data.values()))
        except Exception as e:
            if e.args[0] == 1062:
                sql = "UPDATE sns_data SET like_cnt=%s, reply_cnt=%s, share_cnt=%s, view_cnt=%s, updateDate=%s WHERE url=%s;"
                curs.execute(sql,(data['like_cnt'],data['reply_cnt'],data['share_cnt'],data['view_cnt'],data['updateDate'],data['url']))
                updateNum = updateNum+1
            else:
                print(e)
        else:
            insertNum = insertNum+1
        finally:
            conn.commit()
            conn.close()

    print("총 게시물:",len(all))
    print("update : ",updateNum," / insert : ",insertNum)
    print("==============================================")

if __name__=='__main__':
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    # print(dbKey.keys())
    conn.close()

    start_time = time.time()
    print("페이스북 벤츠 크롤링 시작")
    startCrawling()
    # count = 0
    print("페이스북 벤츠 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
