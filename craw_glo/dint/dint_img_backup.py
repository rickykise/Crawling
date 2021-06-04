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

def dbUpdateIdx(thum, idx):
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "update dint_list set thumbnail=%s where d_idx=%s;"
    curs.execute(sql,(thum,idx))
    conn.commit()

def getTable():
    conn = pymysql.connect(host='49.247.5.169',user='overware',password='uni1004!@',db='union',charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    with conn.cursor() as curs:
        try:
            sql = "SELECT url, d_idx FROM `union`.dint_list where d_idx >= 5648 order by d_idx asc;"
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
def get_save(url, num):
	chromeOptions = webdriver.ChromeOptions()
	chromeOptions.add_argument("disable-infobars")
	driver = webdriver.Chrome("c:\python36\driver\chromedriver", chrome_options=chromeOptions)
	driver.set_window_position(0, 0)
	driver.set_window_size(1080, 1920)

	# alert창 체크
	try:

		driver.get(url)
		WebDriverWait(driver, 1).until(EC.alert_is_present())
		driver.quit()
		print('alert창이 있어 건너뜁니다.')
		return
	except TimeoutException:
		pass

	import pyscreenshot
	try:
		driver.execute_script("window.scrollTo(0, 0);")
                for i in range(0, 5):
                    pyautogui.hotkey('Ctrl', '-')
                    i = i + 1
                    print(i)
		im = pyscreenshot.grab(bbox=(0, 0, 1080, 1920))
		im.save("C:\\Users\\YW\\img\\"+str(num)+'.png')
		im.close()
		# print(time.asctime(), ': ', savefile,'을 저장하였습니다.')
	except:
		pass
	finally:
		driver.quit()

def mkdir():
	dirname = 'c:\img\\'+datetime.datetime.now().strftime('%Y-%m-%d')
	if not os.path.isdir(dirname):
		os.mkdir(dirname)

def main():
    # mkdir()
    getUrl = getTable()

    for u, i in getUrl.items():
        url = u
        num = i[0]
        thum = str(num)+'.png'
        dbUpdateIdx(thum, num)
        get_save(url, num)

    print('완료되었습니다.')

if __name__=='__main__':
    main()
