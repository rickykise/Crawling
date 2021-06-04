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



   # Accept: text/html, application/xhtml+xml, image/jxr, */*
   # Accept-Encoding: gzip, deflate
   # Accept-Language: ko-KR
   # Cookie:
   # Host: www.instagram.com
   # User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko


headers = {
    'Accept' : 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding' : 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': 'ig_did=C1B7EB91-592D-4D9D-AE65-5DD9044C141E; mid=X9q2cQALAAEdM0YPrvqM8JpOE0KZ; ig_nrcb=1; rur=FRC; shbid=6441; shbts=1608169086.4454544; csrftoken=Vhec95N1Vb7VP6bcwuvZPGSO8zj0NeZk; ds_user_id=45148803445; sessionid=45148803445%3ANFZddJwUHnPK6w%3A13',
    'Host': 'www.instagram.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

# 날짜,시간,댓글 처리 함수
def getCount(url,date):
    r = requests.get(url, headers=headers)
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    print(soup)

    data = {
        'like_num' : 0,
        'reply_num' : 0,
        'time' : ''
    }

    textDetail = str(soup)
    data['like_num'] = textDetail.split('edge_media_preview_like":{"count":')[1].split(',')[0].strip()
    data['reply_num'] = textDetail.split('edge_media_to_parent_comment":{"count":')[1].split(',')[0].strip()



    if date:
        from_zone = tz.gettz('UTC');to_zone = tz.gettz('Asia/Seoul');from_zone = tz.tzutc();to_zone = tz.tzlocal()
        central = parse(date).replace(tzinfo=from_zone).astimezone(to_zone)
        data['time'] = central.strftime('%Y-%m-%d %H:%M:%S')

    if data['time'] < datetime.datetime.now().strftime('%Y-%m-%d'):
        print("지남")
    else:
        print("안지남")


    from_zone = tz.gettz('UTC');to_zone = tz.gettz('Asia/Seoul');from_zone = tz.tzutc();to_zone = tz.tzlocal()
    central = parse(date).replace(tzinfo=from_zone).astimezone(to_zone)
    time = central.strftime('%Y-%m-%d %H:%M:%S')

    return data

# 크롤링 함수
def startCrawling():
    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
    try:
        driver.get("https://www.instagram.com/p/CI2Bp6YJC-3/")
        time.sleep(3)

        driver.find_element_by_name('username').send_keys('djfwnrdk@yandex.com')
        driver.find_element_by_name('password').send_keys('unic1004@@')

        driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/button').click()
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
        time.sleep(3)

        driver.get("https://www.instagram.com/p/CI2Bp6YJC-3/")
        time.sleep(3)

        # tagEle = driver.find_element(By.CLASS_NAME,'_2dDPU')
        # tag = tagEle.find_element_by_class_name('JyscU').find_elements_by_class_name('C4VMK')[0].find_elements_by_tag_name('span')[1]
        # text = remove_emoji(tag.text).replace("\n"," ").replace("\t"," ")

        time.sleep(3)

        timeTag = driver.find_element_by_class_name('k_Q0X').find_element_by_tag_name('time')
        resultData = getCount(driver.current_url,timeTag.get_attribute("datetime"))
        print(resultData)
    finally:
        driver.close()

if __name__=='__main__':
    start_time = time.time()

    print("인스타그램 크롤링 시작")
    startCrawling()
    print("인스타그램 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
