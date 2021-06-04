import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
from gloFun import *
from bs4 import BeautifulSoup
import pymysql,time,datetime


def startCrawling(key, keyItem):
    searchKey = getGoogleSearch()
    for k in searchKey:
        keyword = key;cnt_id = keyItem[0];k_start = int(keyItem[1]);k_end = int(keyItem[2]);cnt_keyword='2';

        for c in range(k_start,k_end+1):
            i = 0;check = True;encText = keyword+' '+str(c)+'회 '+k
            googleKey = urllib.parse.quote(encText)
            print('키워드: '+encText)
            link = 'https://yandex.com/search/touch/?text='+googleKey+'&lr=10635&p='

            try:
                while check:
                    if i == 30:
                        break

                    headers = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Cookie': 'Cookie: yandexuid=7981000801606807337; is_gdpr=0; is_gdpr_b=CLuMORDSDygC; yp=1609399339.ygu.1#1622575360.szm.1:2560x1080:768x1280; mda=0; yandex_gid=10635; i=YFXfDUCOQErGOvR5Q/JyfPW+l7B3guFTiZLuD/f6OZw7Gkc2GZsytxDY41RITlAs22bMhBi22HCKayQL4plOI0oLKWo=; my=YwA=; gdpr=0; _ym_uid=1606807353461617184; _ym_isad=2; spravka=dD0xNjA2ODA3Mzc1O2k9MTIxLjE0MC4xNDYuMzE7dT0xNjA2ODA3Mzc1MzI5NDYwMjQ1O2g9YmE2ODkzNDljOTc3ZDY2NGY1YjE1YTkwY2NkNmVlMTU=; _ym_d=1606807365; _ym_visorc_10630330=b; ys=wprid.1606808912154329-1700971414336970637000163-production-app-host-vla-web-yp-145',
                        'Host': 'yandex.com',
                        'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
                    }


                    r = requests.get(link+str(i), headers=headers)
                    i = i+1
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    # print(soup)
                    # text = str(soup)
                    # print(text)
                    # if text.find('IP address: ') != -1:
                    #     time.sleep(50)
                    div = soup.find_all('div', 'serp-item')

                    for item in div:
                        if item.find('a', 'link organic__link'):
                            title = item.find('a', 'link organic__link').text.strip()
                            title_null = titleNull(title)

                            # title 체크
                            googleCheck = googleCheckTitle(title_null, key, cnt_id)
                            if googleCheck == '' or googleCheck == None:
                                continue

                            url = item.find('a', 'link organic__link')['href']
                            url = urllib.parse.unquote(url)

                            # url 체크
                            urlGet = getGoogleUrl()
                            urlCheck = checkGoogleUrl(url, urlGet)
                            if urlCheck['m'] == None:
                                continue

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'yandex',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'russia',
                                'cnt_writer': '',
                                'origin_url': '',
                                'origin_osp': '',
                                'cnt_keyword_nat': None
                            }
                            print(data)
                            print("=================================")

                            # dbResult = insertALLKey(data)
            except:
                pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getGoogleKeyword()

    print("yandex 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("yandex 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
