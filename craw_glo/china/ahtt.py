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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(site):
    i = 0;a = 1;check = True
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            link = 'https://www.ahtt.cc/vodlist/'+site+'/index.htm'
            r = requests.get(link)
        else:
            link = 'https://www.ahtt.cc/vodlist/'+site+'/index-'
            link2 = '.htm'
            r = requests.get(link+str(i)+link2)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        text = str(soup)
        get_text = text.split('</html>')[1].split('<div class="pages">')[0].strip()

        try:
            for item in text:
                try:
                    if a == 9:
                        a = 1
                        break
                    url_text = get_text.split('<ul><a href="')[a].split('"')[0].strip()
                    url = 'https://www.ahtt.cc'+url_text
                    titleSub = get_text.split('<ul><a href="')[a].split(url_text+'" target="_blank">')[1].split('《')[1].split('》')[0].strip()
                    title_check = titleNull(titleSub)
                    a = a+1

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    r = requests.get(url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    div = soup.find_all('div', 'playlist')

                    for item in div:
                        subItem = item.find_all('a')
                        for item in subItem:
                            host_url = 'https://www.ahtt.cc'+item['href']
                            title = titleSub+'_'+item.text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'ahtt',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'china',
                                'cnt_writer': ''
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
                except:
                    a = 1
                    break
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("ahtt 크롤링 시작")
    site = ['18','4']
    for s in site:
        startCrawling(s)
    print("ahtt 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
