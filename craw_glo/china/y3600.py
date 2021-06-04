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

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Host': 'www.y3600.cc',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    link = 'https://www.y3600.cc/'+site+'/index_'
    link2 = '.html'
    link3 = 'https://www.y3600.cc/'+site+'/'
    while check:
        i = i+1
        if i == 30:
            break
        if i == 1:
            r = requests.get(link3, headers=headers)
        else:
            r = requests.get(link+str(i)+link2, headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        ul = soup.find('div', id='content').find_all('ul')

        try:
            for item in ul:
                url = 'https://www.y3600.cc'+item.find('li', 'tit').find('a')['href'].strip()
                titleSub = item.find('li', 'tit').find('a').text.strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                try:
                    driver = webdriver.Chrome("c:\python36\driver\chromedriver")
                    driver.get(url)
                    time.sleep(2)
                    html = driver.find_element_by_class_name("newsleft").get_attribute('innerHTML')
                    soup = BeautifulSoup(html,'html.parser')
                    ul = soup.find_all('ul', re.compile("order+"))

                    for item in ul:
                        li = item.find_all('li')
                        for item in li:
                            host_url = url+'?ing='+item.find('a')['ing']
                            title = titleSub + '_' + item.find('a').text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'y3600',
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
                    pass
                finally:
                    driver.close()
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("y3600 크롤링 시작")
    site = ['hanju', 'hanguozongyi']
    for s in site:
        startCrawling(s)
    print("y3600 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
