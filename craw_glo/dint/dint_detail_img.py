# 이미지 캡쳐
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
# 이미지 저장
import datetime,time,pymysql
import os

def dbUpdateIdx(d_thumbnail, d_url):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "update dint_sbs_list set d_thumbnail=%s, updateDate_d=%s where d_url=%s;"
    curs.execute(sql,(d_thumbnail,now,d_url))
    conn.commit()

def getTable():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT d_url, url, d_num FROM `union`.dint_sbs_list where cate1 = 'MAGAZINE' and d_idx >= '201' order by d_idx asc;"
            curs.execute(sql)
            result = curs.fetchall()
            returnValue = {}
            for i in range(len(result)):
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                    returnValue[key].append(result[i][2])
                else:
                    returnValue.update({key:[result[i][1],result[i][2]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

import pyautogui
def get_save(d_url, d_thumbnail):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("disable-infobars")
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chromeOptions)
    driver.set_window_position(0, 0)
    driver.set_window_size(1920, 1080)

    try:
        driver.get(d_url)
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        driver.quit()
        return
    except TimeoutException:
        pass

    import pyscreenshot
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        im = pyscreenshot.grab(bbox=(0, 0, 1920, 1080))
        im.save("C:\\Users\\YW\\img\\detail\\"+d_thumbnail)
        im.close()
        dbUpdateIdx(d_thumbnail, d_url)
    except:
        pass
    finally:
        driver.quit()

def main():
    getUrl = getTable()

    for u, i in getUrl.items():
        d_url = u
        url = i[0]
        cnt_num = url.split('branduid=')[1].split('&')[0].strip()
        d_num = i[1]
        d_thumbnail = "ca"+cnt_num+'_'+str(d_num)+'.png'
        get_save(d_url, d_thumbnail)

if __name__ == '__main__':
    main()
