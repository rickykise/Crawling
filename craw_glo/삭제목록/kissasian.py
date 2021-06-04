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
from bs4 import BeautifulSoup as bs

def startCrawling():
    i = 0;check = True
    link = 'https://kissasian.sh/Country/South-Korea?page='
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 30:
                break
            link = link+str(i)
            headers = {
                'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Cookie': '__cfduid=dc1151c6a7050e7e9673d963b40616b631561701372; cf_clearance=90a5571c6b45019854479f7426d15a4cbd1188e4-1561701389-1800-150; _ga=GA1.2.2139777417.1561701390; _gid=GA1.2.243343503.1561701390; _gat_gtag_UA_63783416_2=1; ppu_main_c0c197ad1929d1daa75380313517e39d=1; psu_main_33739c336432ac00a30175408abb6640=1; MarketGidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Fkissasian.sh%2FCountry%2FSouth-Korea%3Fpage%3D1%22%2C%22svsds%22%3A2%2C%22TejndEEDj%22%3A%22N_AAxbF21%22%7D%2C%22C262439%22%3A%7B%22page%22%3A2%2C%22time%22%3A1561701590580%7D%7D; 494668b4c0ef4d25bda4e75c27de2817=fbaca65c-fcce-4138-93b7-9a547867d6a4:3:2; ppu_sub_c0c197ad1929d1daa75380313517e39d=1; psu_sub_33739c336432ac00a30175408abb6640=1',
                'Host': 'kissasian.sh',
                'Referer': link,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
            }
            post_one = s.get(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            print(soup)
            div = soup.find('div', 'list-drama').find_all('div')

            try:
                for item in div:
                    url = 'https://kissasian.sh'+item.find('a')['href']
                    titleSub = item.find('span', 'title')
                    title_check = titleNull(titleSub)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    post_two = s.get(url, headers=headers)
                    soup = bs(post_two.text, 'html.parser')
                    tr = soup.find('table', 'listing').find_all('tr')

                    for item in tr:
                        td = item.find_all('td')
                        if len(td) != 0:
                            cnt_url = 'https://kissasian.sh'+item.find('a')['href']
                            cnt_num = cnt_url.split('id=')[1]
                            title = item.find('a').text.strip()
                            title_null = titleNull(title)

                            r = requests.get(host_url)
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")
                            host_cnt = len(soup.find('select', id='selectServer').find_all('option'))

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'kissasian',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': host_cnt,
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'philippines',
                                'cnt_writer': ''
                            }
                            print(data)
                            print("=================================")

                            # dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("kissasian 크롤링 시작")
    startCrawling()
    print("kissasian 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
