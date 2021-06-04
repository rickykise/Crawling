import requests,re
import pymysql,time,datetime
import pyautogui
import datetime
import subprocess
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from bs4 import BeautifulSoup

def startCrawling():
    dis = subprocess.call("taskkill /f /im cmd.exe", shell=True)

if __name__=='__main__':
    start_time = time.time()

    print("cmd_kill 크롤링 시작")
    startCrawling()
    print("cmd_kill 크롤링 끝")
