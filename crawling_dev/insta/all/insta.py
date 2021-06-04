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

headers = {
    'Accept' : 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': 'rur=FRC; ig_did=748008CB-E24F-492C-98AB-FBFDB4B3D951; mid=X9v9pgALAAGWaSO7JR2C1oEIatBT; csrftoken=Q5gDYTo8nJUPV1QL4ryIpW408QEQCSTV; ds_user_id=44959486549; ig_nrcb=1; sessionid=44959486549%3Ahdo3Rco7Vx5iZS%3A27',
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# 날짜,시간,댓글 처리 함수
def getCount(url,date):
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")

    data = {
        'like_num' : 0,
        'reply_num' : 0
    }

    textDetail = str(soup)
    data['like_num'] = textDetail.split('edge_media_preview_like":{"count":')[1].split(',')[0].strip()
    data['reply_num'] = textDetail.split('edge_media_to_parent_comment":{"count":')[1].split(',')[0].strip()

    return data

# 크롤링 함수
def startCrawling():
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        driver.get("https://www.instagram.com/explore/tags/porter/")
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]').click()
        time.sleep(5)

        # hourGet = datetime.datetime.now().strftime('%H:%M:%S')
        # if hourGet >= '18:00:00':
        #     driver.find_element_by_name('username').send_keys('thdxotjq@yandex.com')
        #     driver.find_element_by_name('password').send_keys('unic1004!!')
        # else:
        #     driver.find_element_by_name('username').send_keys('dusdockarus@yandex.com')
        #     driver.find_element_by_name('password').send_keys('unic1004!@')

        driver.find_element_by_name('username').send_keys('dutlsrkdfla@yandex.com')
        driver.find_element_by_name('password').send_keys('unic1004@@')

        driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(3)

        conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        dbKey = getSearchKey(conn,curs)
        conn.close()

        for key in dbKey.keys():
            if key == '009240':
                continue
            print("키워드 : "+key)
            driver.get("https://www.instagram.com/explore/tags/"+key.replace(' ','')+"/")
            time.sleep(3)

            try:
                driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div[1]/div[2]').click()
                time.sleep(3)

                # 인기게시물
                for i in range(0, 9) :
                    try:
                        time.sleep(3)
                        tagEle = driver.find_element(By.CLASS_NAME,'_2dDPU')
                        tagEle.find_element(By.CLASS_NAME,'_65Bje').click()
                        i +=1
                    except:
                        break
            except:
                continue

            # 최근게시물
            while True:
                try:
                    time.sleep(3)
                    tagEle = driver.find_element(By.CLASS_NAME,'_2dDPU')
                    tag = tagEle.find_element_by_class_name('JyscU').find_elements_by_class_name('C4VMK')[0].find_elements_by_tag_name('span')[1]
                    text = remove_emoji(tag.text).replace("\n"," ").replace("\t"," ")
                    timeTag = tagEle.find_element_by_class_name('k_Q0X').find_element_by_tag_name('time')
                    date = timeTag.get_attribute("datetime")
                    from_zone = tz.gettz('UTC');to_zone = tz.gettz('Asia/Seoul');from_zone = tz.tzutc();to_zone = tz.tzlocal()
                    central = parse(date).replace(tzinfo=from_zone).astimezone(to_zone)
                    writeDate = central.strftime('%Y-%m-%d %H:%M:%S')
                    if writeDate < datetime.datetime.now().strftime('%Y-%m-%d'): break
                    result = checkKeyword(text,dbKey[key]['add'],dbKey[key]['del'])

                    if result:
                        timeTag = tagEle.find_element_by_class_name('k_Q0X').find_element_by_tag_name('time')
                        date = timeTag.get_attribute("datetime")
                        resultData = getCount(driver.current_url,timeTag.get_attribute("datetime"))

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
                                'sns_writer' : tagEle.find_element_by_class_name('JyscU').find_elements_by_class_name('C4VMK')[0].find_element_by_tag_name('span').text,
                                'sns_content' : text,
                                'title_key': dbKey[key]['add'][0],
                                'keyword' : putKey,
                                'url' : tagEle.find_element_by_class_name('k_Q0X').find_element_by_class_name('c-Yi7').get_attribute("href"),
                                'like_cnt' : resultData['like_num'],
                                'reply_cnt' : resultData['reply_num'],
                                'share_cnt' : 0,
                                'writeDate' : writeDate,
                                'createDate': now,
                                'updateDate': now
                            }
                            data['sns_title'] = data['sns_writer']+"#"+(data['keyword'].replace("#",""))
                            print(data)
                            print("=======================")

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
                            else:
                                pass
                        finally:
                            conn.close()
                            conn2.close()
                except:
                    driver.find_element(By.CLASS_NAME,'_65Bje').click()
                    continue
                driver.find_element(By.CLASS_NAME,'_65Bje').click()
    # except: pass
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("인스타그램 크롤링 시작")
    startCrawling()
    print("인스타그램 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
