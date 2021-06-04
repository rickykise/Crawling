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

def dbUpdateIdx(thum, url):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sql = "update dint_sbs_list set thumbnail=%s, updateDate=%s where url=%s;"
    curs.execute(sql,(thum,now,url))
    conn.commit()

def getTable():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT url, d_idx FROM `union`.dint_sbs_list where cate1 = 'MAGAZINE' group by url order by d_idx asc;"
            curs.execute(sql)
            result = curs.fetchall()
            returnValue = {}
            for i in range(len(result)):
                key = result[i][0]
                if key in returnValue:
                    returnValue[key].append(result[i][1])
                else:
                    returnValue.update({key:[result[i][1]]})
            # print(returnValue)
        finally:
            conn.close()
            return returnValue

import pyautogui
def get_save(url, thum):
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("disable-infobars")
    driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chromeOptions)
    driver.set_window_position(0, 0)
    driver.set_window_size(1080, 1920)


    try:
        driver.get(url)
        WebDriverWait(driver, 1).until(EC.alert_is_present())
        driver.quit()
        return
    except TimeoutException:
        pass

    import pyscreenshot
    try:
        for i in range(0, 5):
            pyautogui.hotkey('Ctrl', '-')
            time.sleep(1)
            i = i + 1
            # print(i)
        driver.execute_script("window.scrollTo(0, 0);")
        im = pyscreenshot.grab(bbox=(0, 0, 1080, 1920))
        im.save("C:\\Users\\YW\\img\\"+thum)
        im.close()
        dbUpdateIdx(thum, url)
    except:
        pass
    finally:
        driver.quit()

def main():
    getUrl = getTable()
    for u, i in getUrl.items():
        url = u
        cnt_num = u.split('branduid=')[1].split('&')[0].strip()
        thum = "ca"+cnt_num+'.png'
        get_save(url, thum)

if __name__ == '__main__':
    main()
