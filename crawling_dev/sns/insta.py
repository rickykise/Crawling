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
        count = metaTag.get("content").split("-")[0].split(",")
        data['like_num'] = int(''.join(list(filter(str.isdigit,count[0]))))
        data['reply_num'] = int(''.join(list(filter(str.isdigit,count[1]))))

    if date:
        from_zone = tz.gettz('UTC');to_zone = tz.gettz('Asia/Seoul');from_zone = tz.tzutc();to_zone = tz.tzlocal()
        central = parse(date).replace(tzinfo=from_zone).astimezone(to_zone)
        data['time'] = central.strftime('%Y-%m-%d %H:%M:%S')

    return data

# 크롤링 함수
def startCrawling(key):
    key = '김상호'
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        print("키워드 : "+key)
        updateNum = 0;insertNum = 0
        driver.get("https://www.instagram.com/explore/tags/"+key.replace(' ','')+"/")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]').click()
        # 인기게시물
        for i in range(0, 9) :
            try:
                time.sleep(3)
                tagEle = driver.find_element(By.CLASS_NAME,'_2dDPU')
                tagEle.find_element(By.CLASS_NAME,'_65Bje').click()
                i +=1
            except:
                break

        # 최근게시물
        while True:
            time.sleep(3)
            tagEle = driver.find_element(By.CLASS_NAME,'_2dDPU')
            tag = tagEle.find_element_by_class_name('JyscU').find_elements_by_class_name('gElp9')[0].find_element_by_tag_name('span')
            text = remove_emoji(tag.text).replace("\n"," ").replace("\t"," ")
            print(text)
            result = checkKeyword(text,dbKey[key]['add'],dbKey[key]['del'])

            if result:
                timeTag = tagEle.find_element_by_class_name('k_Q0X').find_element_by_tag_name('time')
                resultData = getCount(driver.current_url,timeTag.get_attribute("datetime"))
                # print(resultData['time'])
                if resultData['time'] < datetime.datetime.now().strftime('%Y-%m-%d'): break
                # if resultData['time'] <= '2018-08-10' : break

                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'sns_name': 'instagram',
                    'sns_title': '',
                    'sns_writer' : tagEle.find_element_by_class_name('e1e1d').find_element_by_class_name('FPmhX').text,
                    'sns_content' : text,
                    'title_key': dbKey[key]['add'][0],
                    'url' : tagEle.find_element_by_class_name('k_Q0X').find_element_by_class_name('c-Yi7').get_attribute("href"),
                    'like_cnt' : resultData['like_num'],
                    'reply_cnt' : resultData['reply_num'],
                    'share_cnt' : 0,
                    'writeDate' : resultData['time'],
                    'createDate': now,
                    'updateDate': now
                }
                print(data)
                print("=======================")

                conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
                conn2 = pymysql.connect(host='211.193.58.218',user='soas',password='qwer1234',db='union',charset='utf8')
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    curs2 = conn2.cursor(pymysql.cursors.DictCursor)
                    putKey = getPutKeyword(text,dbKey[key]['add'])
                    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    data = {
                        'sns_name': 'instagram',
                        'sns_title': '',
                        'sns_writer' : tagEle.find_element_by_class_name('e1e1d').find_element_by_class_name('FPmhX').text,
                        'sns_content' : text,
                        'title_key': dbKey[key]['add'][0],
                        'keyword' : putKey,
                        'url' : tagEle.find_element_by_class_name('k_Q0X').find_element_by_class_name('c-Yi7').get_attribute("href"),
                        'like_cnt' : resultData['like_num'],
                        'reply_cnt' : resultData['reply_num'],
                        'share_cnt' : 0,
                        'writeDate' : resultData['time'],
                        'createDate': now,
                        'updateDate': now
                    }
                    data['sns_title'] = data['sns_writer']+"#"+(data['keyword'].replace("#",""))
                    # print(data)

                    placeholders = ', '.join(['%s'] * len(data))
                    columns = ', '.join(data.keys())
                    sql = "INSERT INTO sns_data ( %s ) VALUES ( %s );" % (columns, placeholders)
                    curs.execute(sql, list(data.values()))
                    conn.commit()
                    curs2.execute(sql, list(data.values()))
                    conn2.commit()
                except Exception as e:
                    # if e.args[0] == 1062: break
                    if e.args[0] == 1062:
                        sql = "UPDATE sns_data SET title_key=%s, like_cnt=%s, reply_cnt=%s, updateDate=%s WHERE url=%s;"
                        curs.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                        curs2.execute(sql,(data['title_key'],data['like_cnt'],data['reply_cnt'],data['updateDate'],data['url']))
                        updateNum = updateNum+1
                    else:
                        pass
                finally:
                    conn.close()
                    conn2.close()
            driver.find_element(By.CLASS_NAME,'_65Bje').click()
    # except: pass
    finally:
        driver.close()

    print("insert : ",insertNum,"/update :",updateNum)
    print("=======================")

if __name__=='__main__':
    start_time = time.time()
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    dbKey = getSearchKey(conn,curs)
    conn.close()

    print("인스타그램 크롤링 시작")
    for k in dbKey.keys():
        # if dbKey[k]['add'][0] == '암수살인':
        #     startCrawling(k)
        startCrawling(k)
    print("인스타그램 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
