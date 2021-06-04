# 이미지 캡쳐
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
from tkinter.filedialog import askopenfilename
import requests
import pandas as pd
import pyautogui
import subprocess
# 이미지 저장
import datetime,time,pymysql
import os
import pyscreenshot

def main():
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("disable-infobars")
    driver = webdriver.Chrome('C:\python36\driver\chromedriver.exe', chrome_options=chromeOptions)
    driver.set_window_position(0, 0)
    driver.set_window_size(1080, 1748)

    try:
        driver.get("https://www.naver.com/")
        time.sleep(2)
        im = pyscreenshot.grab(bbox=(0, 0, 1080, 1918))
        im.save("c:/img/test.png")
        im.close()
        dis = subprocess.call("pscp -pw sms@unionc c:/img/test.png root@49.247.5.169:/usr/local/img/"+datetime.datetime.now().strftime('%Y-%m-%d')+"/", shell=True)
        print("pscp -pw sms@unionc c:/img/test.png root@49.247.5.169:/usr/local/img/"+datetime.datetime.now().strftime('%Y-%m-%d')+"/")
    # except Exception as e:
    #     pass
    finally:
        driver.quit()

if __name__=='__main__':
    print('시작')
    main()
    print('끝')
