import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
import pandas
from horoFun import *
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from bs4 import BeautifulSoup

def startCrawling():
    i = 0;check = True
    sign = {
        'Aries': '1',
        'Taurus': '2',
        'Gemini': '3',
        'Cancer': '4',
        'Leo': '5',
        'Virgo': '6',
        'Libra': '7',
        'Scorpio': '8',
        'Sagittarius': '9',
        'Capricorn': '10',
        'Aquarius': '11',
        'Pisces': '12'
    }
    # print(s[0]) : 별자리
    # print(s[1]) : 별자리 키값

    for s in sign.items():
        try:
            loves = ['single', 'couple']
            for item in loves:
                link = 'https://www.horoscope.com/us/horoscopes/love/horoscope-love-weekly-'+item+'.aspx?sign='+s[1]
                r = requests.get(link)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = soup.find('div', 'main-horoscope').find('p').text.replace('\xa0', '').strip()

                monthCheck = text.split(' ')[0].strip()
                month = dateFormat(monthCheck)
                dateCheck = text.split(' - ')[0].replace(monthCheck, month)
                writeDate = datetime.datetime.strptime(dateCheck.split('-')[0].strip(), "%m %d, %Y").strftime('%Y-%m-%d')
                writeDate2 = datetime.datetime.strptime(dateCheck.split('-')[1].split(' - ')[0].strip(), "%m %d, %Y").strftime('%Y-%m-%d')

                # monthCheck2 = text.split('-')[1].split(' ')[0].strip()
                # month2 = dateFormat(monthCheck2)
                # dateCheck2 = text.split(' - ')[0].replace(monthCheck2, month2)
                # print(dateCheck2)
                # writeDate2 = datetime.datetime.strptime(dateCheck2, "%m %d, %Y").strftime('%Y-%m-%d')


                data = {
                    'horoscope_cons': s[0],
                    'horoscope_cate': 'love',
                    'horoscope_love': item,
                    'horoscope_date' : 'weekly',
                    'horoscope_content': text,
                    'writeDate':writeDate+' - '+writeDate2
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)

                link2 = 'https://www.horoscope.com/us/horoscopes/love/horoscope-love-monthly-'+item+'.aspx?sign='+s[1]
                r = requests.get(link2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = soup.find('div', 'main-horoscope').find('p').text.replace('\xa0', '').strip()
                monthCheck = text.split(' ')[0].strip()
                month = dateFormat(monthCheck)
                dateCheck = text.split(' - ')[0].replace(monthCheck, month)
                writeDate = datetime.datetime.strptime(dateCheck, "%m %Y").strftime('%Y-%m')

                data = {
                    'horoscope_cons': s[0],
                    'horoscope_cate': 'love',
                    'horoscope_love': item,
                    'horoscope_date' : 'monthly',
                    'horoscope_content': text,
                    'writeDate': writeDate
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)

            dt_index = pandas.date_range(start='20190622', end='20200623')
            dt_list = dt_index.strftime("%Y%m%d").tolist()

            for i in dt_list:
                link3 = 'https://www.horoscope.com/us/horoscopes/love/horoscope-archive.aspx?sign='+s[1]+'&laDate='+i
                r = requests.get(link3)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                text = soup.find('div', 'main-horoscope').find('p').text.replace('\xa0', '').strip()
                monthCheck = text.split(' ')[0].strip()
                month = dateFormat(monthCheck)
                dateCheck = text.split(' - ')[0].replace(monthCheck, month)
                writeDate = datetime.datetime.strptime(dateCheck, "%m %d, %Y").strftime('%Y-%m-%d')

                data = {
                    'horoscope_cons': s[0],
                    'horoscope_cate': 'love',
                    'horoscope_love': None,
                    'horoscope_date' : 'daily',
                    'horoscope_content': text,
                    'writeDate': writeDate
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()

    print("horoscope_love 크롤링 시작")
    startCrawling()
    print("horoscope_love 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
