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
            sql = "SELECT url, d_url FROM `union`.dint_sbs_list where d_url is not null group by url order by d_idx asc;"
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

def get_thum(d_url):
    if d_url.find('tvspon/') != -1:
        d_thum = d_url.split('tvspon/')[1].strip()
        if d_thum.count('/') == 1:
            split_thum1 = d_thum.split('/')[1].split('_')[0].strip()
            split_thum2 = d_thum.split('/')[1].split(split_thum1)[1].split('_')[1].split('_')[0].strip()
            d_thumbnail = split_thum1+'_'+split_thum2

        else:
            split_thum1 = d_thum.split('_')[0].strip()
            split_thum2 = d_thum.split(split_thum1)[1].split('_')[1].split('_')[0].strip()
            d_thumbnail = split_thum1+'_'+split_thum2
    else:
        d_thum = d_url.split('board/')[1].strip()
        split_thum1 = d_thum.split('_')[0].strip()
        split_thum2 = d_thum.split(split_thum1)[1].split('_')[1].split('_')[0].strip()
        d_thumbnail = split_thum1+'_'+split_thum2
    d_thumbnail = d_thumbnail.replace('.jpg', '').strip()
    if d_thumbnail.find('-') != -1:
        d_thumbnail = d_thumbnail.split('_')[0].strip()

    return d_thumbnail

def main():
    getUrl = getTable()

    for u, i in getUrl.items():
        url = u
        d_url = i[0]
        d_thum = get_thum(d_url)
        thum = d_thum+'.png'
        get_save(url, thum)

if __name__ == '__main__':
    main()
