# 네이버 검색 Open API - web 검색
import datetime,pymysql,time,math
import urllib.request
import requests
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from portal_api import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def getlastDate(key):
    lastDate = None
    try:
        conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
        curs = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select writeDate from portal_data where portal_type='score' and keyword=%s order by writeDate desc limit 1;"
        curs.execute(sql, key)
        result = curs.fetchone()
        if result:
            lastDate = result['writeDate'].strftime('%Y-%m-%d %H:%M')
        else:
            lastDate = 'f'
    finally:
        conn.close()

    return lastDate

def startCrawling(key):
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        # lastDate = getlastDate(key)
        # if not lastDate: continue

        link = "http://movie.naver.com/movie/bi/mi/point.nhn?code="
        driver.get(link+mkey[key])
        WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'pointAfterListIframe')))
        ele = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="orderCheckbox"]/ul/li[2]/a')))
        ele.click();time.sleep(3)
        insertNum = 0;check = True;paging = 1

        while check:
            html = driver.find_element_by_class_name('score_result').get_attribute('innerHTML')
            soup = BeautifulSoup(html,"html.parser")
            [x.extract() for x in soup.findAll("span","ico_viewer")]
            findLI = soup.find("ul").find_all("li")

            for item in findLI:
                conn = pymysql.connect(host='192.168.0.16',user='soas',password='qwer1234',db='union',charset='utf8')
                info = item.find("div","score_reple")
                score_num = int(item.find("div","star_score").find("em").get_text())
                now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data = {
                    'portal_type': 'score',
                    'portal_name': 'naver',
                    'portal_title': info.find("p").get_text(),
                    'deviceType': 1,
                    'score': score_num,
                    'textType': (score_num>=8 and "좋은글") or (score_num>=5 and "관심글") or (score_num>=2 and "나쁜글") or (score_num>=1 and "악성글"),
                    'writer': info.find("dt").find_all("em")[0].find("span").get_text(),
                    'writeDate': info.find("dt").find_all("em")[1].get_text().replace(".","-"),
                    'title_key': getMainKey(conn,key),
                    'keyword': key,
                    'keyword_type': '영화',
                    'url':'naver.'+datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(insertNum),
                    'createDate': now,
                    'updateDate':now
                }
                data['portal_title'] = (len(data['portal_title']) > 255) and data['portal_title'][:255] or data['portal_title']
                data['portal_title'] = data['portal_title'].replace("'",'"')
                # if lastDate != 'f':
                #     if (data['writeDate'].find(lastDate) != -1) or (data['writeDate'] < lastDate):
                #         check = False;break
                try:
                    curs = conn.cursor(pymysql.cursors.DictCursor)
                    placeholders = ', '.join(['%s'] * len(data))
                    columns = ', '.join(data.keys())
                    query = "SELECT * FROM portal_data WHERE portal_title=\'%s\' and keyword=\'%s\' and writeDate=\'%s\'" % (data['portal_title'],data['keyword'],data['writeDate'])
                    sql = "INSERT INTO portal_data(%s) SELECT %s from dual WHERE NOT EXISTS (%s);" % (columns, placeholders, query)
                    curs.execute(sql, list(data.values()))
                    conn.commit()
                except Exception as e:
                    if e.args[0] != 1062:
                        print("에러 :",e)
                    # else:
                    #     check = False;break
                finally:
                    conn.close()

            if check:
                paging = paging+1
                ele = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pagerTagAnchor'+str(paging)+'"]')))
                ele.click();time.sleep(3)
    except TimeoutException as ex:
        print("**********TimeoutException*************")
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()
    mkey = {'버닝':'155263'}
    print("네이버 영화 평점 크롤링 시작")
    for key in mkey:
        print("키워드 : "+key)
        startCrawling(key)
    print("네이버 영화 평점 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
