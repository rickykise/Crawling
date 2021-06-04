import requests,re
import pymysql,time,datetime
import urllib.parse
import urllib.request
import sys,os
import smtplib
from datetime import date, timedelta
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

# site_url 가져오는 함수
def getOspUrl():
    result = None
    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site',port=3307,charset='utf8')
    with conn.cursor() as curs:
        sql = "select osp_url, osp_id, osp_nat from osp_list where osp_state = '1' order by n_idx asc;"
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

        return returnValue

def put(returnValue):
    # print(returnValue)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fromaddr = "develop@unionc.co.kr"
    toaddr = ["sms@unionc.co.kr", 'siteen@unionc.co.kr', "kdh7342@unionc.co.kr"]
    # toaddr = "rickykise@naver.com"
    if returnValue == [] :
        msg = "VPN 검출된 osp가 없습니다."
    else:
        msg = "\n".join(returnValue)

    id = "rickykise1"
    password="duddnchl1125"

    smtp = smtplib.SMTP_SSL('smtp.daum.net:465')
    smtp.login(id, password)
    msg = MIMEText(msg)
    msg['Subject'] = "VPN - OSP폐쇄 - "+now
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    # msg['To'] = toaddr
    smtp.sendmail(fromaddr, toaddr, msg.as_string())
    smtp.quit()
    print("Done")

def startCrawling():
    i = 0;check = True;checkNum = 0;returnValue = []
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    getUrl = getOspUrl()
    for url, chekc_item in getUrl.items():
        osp_id = chekc_item[0]
        osp_nat = chekc_item[1]
        try:
            r = requests.get(url, timeout = 2)
            urlState = r.status_code
            # print(url)
            # print(urlState)
            # print('===========================')
            if urlState != 200 and urlState != 520 and urlState != 503:
                returnValue.append(url)
                returnValue.append(osp_id)
                returnValue.append(osp_nat)
                returnValue.append(now)
                returnValue.append(' ')
        except:
            pass

    # print(returnValue)
    put(returnValue)

if __name__=='__main__':
    start_time = time.time()
    print("osp_list_vpn 재검수 시작")
    startCrawling()
    print("osp_list_vpn 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
