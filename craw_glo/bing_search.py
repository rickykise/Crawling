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
            i = 1;check = True;encText = keyword+' '+str(c)+'회 '+k
            googleKey = urllib.parse.quote(encText)
            print('키워드: '+encText)
            link = 'https://www.bing.com/search?q='+googleKey+'&qs=n&sp=-1&pq='+googleKey+'&sc=0-15&sk=&cvid=C4100CE1A2CE46279B974585B728A936&first='

            try:
                while check:
                    headers = {
                        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'ko-KR',
                        'Host': 'www.bing.com',
                        'Referer': link+str(i),
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                    }
                    r = requests.get(link+str(i), headers=headers)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)
                    div = soup.find_all('li', 'b_algo')

                    for item in div:
                        if item.find('a'):
                            title = item.find('a').text.strip()
                            title_null = titleNull(title)

                            # title 체크
                            googleCheck = googleCheckTitle(title_null, key, cnt_id)
                            if googleCheck == '' or googleCheck == None:
                                continue

                            url = item.find('a')['href']
                            url = urllib.parse.unquote(url)

                            # url 체크
                            # urlGet = getGoogleUrl()
                            # urlCheck = checkGoogleUrl(url, urlGet)
                            # if urlCheck['m'] == None:
                            #     continue

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'bing',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'unitedstates',
                                'cnt_writer': '',
                                'origin_url': '',
                                'origin_osp': '',
                                'cnt_keyword_nat': None
                            }
                            print(data)
                            print("=================================")

                            # dbResult = insertALLKey(data)

                    i = i+10
                    if i == 30:
                        check=False;break
            except:
                pass

if __name__=='__main__':
    start_time = time.time()
    getKey = getGoogleKeyword()

    print("bing 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("bing 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
