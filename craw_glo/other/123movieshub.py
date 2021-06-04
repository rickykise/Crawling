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

def startCrawling():
    i = 0;a = 1;check = True
    link = 'https://123movieshub.town/country/kr/'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'ml-item')

        try:
            for item in div:
                url = 'https://123movieshub.town' + item.find('a')['href']
                data_id = item['data-movie-id']
                titleSub = item.find('img')['alt']
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_check = titleNull(titleSub)

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
                url2 = soup.find('div', id='mv-info').find('a')['href']

                ajax_url = 'https://123movieshub.town/ajax/movie_episodes/'+data_id
                try:
                    r = requests.get(ajax_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    text = str(soup)

                    for item in text:
                        ajax_text = text.split('javascript:void(0)')[a].split('&lt;')[0].replace('\\', '')
                        host_url = url2+'?ep=' + ajax_text.split('ep-')[1].split('"')[0]
                        title = titleSub+'_'+ajax_text.split("title='")[1].split('"')[1].split('"')[0].replace("Episode'>", '').strip()
                        title_null = titleNull(title)
                        a = a+1


                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '123movieshub',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'other',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
                except:
                    continue
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("123movieshub 크롤링 시작")
    startCrawling()
    print("123movieshub 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
