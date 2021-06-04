import requests,re
import pymysql,time,datetime
import pyautogui
import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup
from imgCheck import *

def startCrawling():
    cnt_id = 'applefile'
    url = 'http://applefile.com/contents/board_view.php?idx=16114671'
    data = imgCheck(cnt_id,url)
    print(cnt_id)
    print(data)

if __name__=='__main__':
    start_time = time.time()

    print("test 크롤링 시작")
    startCrawling()
    print("test 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
