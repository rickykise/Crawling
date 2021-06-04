import requests,re
import pymysql,time,datetime
import datetime
import subprocess

def startCrawling():
    dis = subprocess.call("taskkill /f /im cmd.exe /T", shell=True)
    dis = subprocess.call("taskkill /f /im python.exe /T", shell=True)

if __name__=='__main__':
    start_time = time.time()

    print("cmd_kill 크롤링 시작")
    startCrawling()
    print("cmd_kill 크롤링 끝")
