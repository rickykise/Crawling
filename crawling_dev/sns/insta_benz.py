# 인스타그램 크롤링
import datetime, time
import requests
import pymysql
import re
from snsFun import *
from datetime import date, timedelta
from dateutil import tz
from dateutil.parser import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 날짜,시간,댓글 처리 함수
def getCount(url,date):
    r = requests.get(url)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    data = {
        'like_num' : 0,
        'reply_num' : 0,
        'time' : ''
    }
    metaTag = soup.find(property="og:description")
    if metaTag:
        #content="좋아요 2,406개, 댓글 194개 -
        count = metaTag.get("content").split("-")[0].split("s,")
        data['like_num'] = int(''.join(list(filter(str.isdigit,count[0]))))
        data['reply_num'] = int(''.join(list(filter(str.isdigit,count[1]))))

    if date:
        from_zone = tz.gettz('UTC');to_zone = tz.gettz('Asia/Seoul');from_zone = tz.tzutc();to_zone = tz.tzlocal()
        central = parse(date).replace(tzinfo=from_zone).astimezone(to_zone)
        data['time'] = central.strftime('%Y-%m-%d %H:%M:%S')

    return data

# 크롤링 함수
def startCrawling():
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        print("키워드 : 벤츠")
        updateNum = 0;insertNum = 0
        driver.get("https://www.instagram.com/mercedesbenzkr/")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div[1]/div[1]/a/div/div[2]').click()
        time.sleep(3)
        # 최근게시물
        while True:
            time.sleep(3)
            tagEle = driver.find_element(By.CLASS_NAME,'_pfyik')
            tag = tagEle.find_element_by_class_name('_b0tqa').find_elements_by_class_name('_ezgzd')[0].find_element_by_tag_name('span')
            text = remove_emoji(tag.text).replace("\n"," ").replace("\t"," ")
            timeTag = tagEle.find_element_by_class_name('_djdmk').find_element_by_tag_name('time')
            resultData = getCount(driver.current_url,timeTag.get_attribute("datetime"))
            # if resultData['time'] < datetime.datetime.now().strftime('%Y-%m-%d'): break
            # print(resultData['time'])
            if resultData['time'] <= '2018-04-01' : break

            conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
            try:
                curs = conn.cursor(pymysql.cursors.DictCursor)
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'sns_name': 'instagram',
                    'sns_title': '',
                    'sns_writer' : tagEle.find_element_by_class_name('_7b8eu').find_element_by_class_name('_2g7d5').text,
                    'sns_content' : text,
                    'title_key': '벤츠',
                    'keyword' : '벤츠',
                    'url' : tagEle.find_element_by_class_name('_djdmk').get_attribute("href"),
                    'like_cnt' : resultData['like_num'],
                    'reply_cnt' : resultData['reply_num'],
                    'share_cnt' : 0,
                    'writeDate' : resultData['time'],
                    'createDate': now,
                    'updateDate': now
                }
                data['sns_title'] = data['sns_writer']+"#벤츠"

                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                curs.execute(sql, list(data.values()))
                conn.commit()
            except Exception as e:
                # if e.args[0] == 1062: break
                if e.args[0] == 1062:
                    sql = "UPDATE sns_data SET like_cnt=%s, reply_cnt=%s, updateDate=%s WHERE url=%s;"
                    curs.execute(sql,(data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                    conn.commit()
                    updateNum = updateNum+1
                else:
                    pass
            finally:
                conn.close()
            driver.find_element(By.CLASS_NAME,'coreSpriteRightPaginationArrow').click()
    except: pass
    finally:
        driver.close()

    print("insert : ",insertNum,"/update :",updateNum)
    print("=======================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("인스타그램 벤츠 크롤링 시작")
    startCrawling()
    print("인스타그램 벤츠 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
