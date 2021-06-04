import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    getUrl = getOspVpnUrl()
    for url, chekc_item in getUrl.items():
        idx = chekc_item[0]
        osp_state = 0
        # print(url)
        try:
            r = requests.get(url)
            urlState = r.status_code
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            text = str(soup)
            if urlState == 200:
                if soup.find('title').text.find('유해정보사이트에 대한 차단') != -1:
                    osp_state = 0
                    # print('차단')
                else:
                    continue
                    # print('정상')
            elif text.find('방송통신심의위원회') != -1:
                osp_state = 0
                # print('차단')
            elif urlState == 404:
                osp_state = 0
                # print('폐쇄')
            elif urlState != 200 and urlState != 520 and urlState != 503:
                osp_state = 0
                # print('변경')
            # print(osp_state)
            # print("=================================")
            stateVpnUpdate(osp_state,idx)
        except:
            osp_state = 0
            # print(osp_state)
            # print("=================================")
            stateVpnUpdate(osp_state,idx)
            continue

if __name__=='__main__':
    start_time = time.time()
    print("osp_list 재검수 시작")
    startCrawling()
    print("osp_list 재검수 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
