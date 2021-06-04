import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from similarwebFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from spyse import spyse

def startCrawling(url):
    i = 0;check = True
    url = url.replace('https://', '').replace('http://', '')
    with requests.Session() as s:
        link = "https://www.alexa.com/siteinfo/" + url
        post_one  = s.get(link)
        soup = bs(post_one.text, 'html.parser')
        div = soup.find_all('div', 'site')

        for item in div:
            try:
                if item.find('a'):
                    check_text = item.find('a').text.strip()
                    if check_text.find('Keyword') != -1 or check_text.find('Optimization') != -1:
                        continue
                    osp_url = "https://"+item.find('a').text.strip()
                    if osp_url.find('About Sites') != -1:
                        continue
                    dot = osp_url.count('.')
                    if dot == 2:
                        if osp_url.find('co.kr') != -1:
                            osp_id = item.find('a').text.split('.')[0].strip()
                        else:
                            osp_id = item.find('a').text.split('.')[1].split('.')[0].strip()
                    else:
                        osp_id = item.find('a').text.split('.')[0].strip()

                    # html 체크
                    check_ospurl = check_url(osp_url)
                    if check_ospurl == True:
                        try:
                            subUrl = osp_url.replace('https://', '').replace('http://', '').replace('www.', '')
                            spy = spyse('2Dz6uSLzSjbcjQE39F41Mc7ctZs3_Eru')
                            subdomains = spy.subdomains(subUrl, param='domain')
                            subText = str(subdomains)
                            osp_s_nat = subText.split("country': {'name': '")[1].split("'")[0].strip()
                            osp_s_nat = change_Nat(osp_s_nat)
                            osp_isp = subText.split("organization': '")[1].split("'")[0].strip()
                        except:
                            osp_s_nat = None
                            osp_isp = None

                        try:
                            natUrl = osp_url.replace('https://', '').replace('http://', '')
                            natLink = "https://www.alexa.com/siteinfo/" + natUrl
                            post_two  = requests.get(natLink)
                            soup2 = bs(post_two.text, 'html.parser')
                            osp_nat = soup2.find('section', 'country').find('li').find('div').text.encode('unicode-escape').decode('utf-8').split('\\xa0')[1].strip()
                            osp_nat = change_Nat(osp_nat)
                        except:
                            osp_nat = None

                        data = {
                            'osp_id': osp_id,
                            'osp_url': osp_url,
                            'osp_nat': osp_nat,
                            'osp_s_nat': osp_s_nat,
                            'osp_isp': osp_isp
                        }
                        print(data)
                        print("=================================")
                        # dbInResult = similarwebInsert(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()
    getUrl = getOspTR()

    print("alexa 크롤링 시작")
    for u in getUrl:
        startCrawling(u)
    print("alexa 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
