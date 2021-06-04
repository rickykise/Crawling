import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = 'http://www.ccv5.com/a/18.html'
   
    r = requests.get(link)
    r.encoding = r.apparent_encoding
    c = r.text
    soup = BeautifulSoup(c,"html.parser")
    div = soup.find('div','m_main').find_all('div','newtype')

    for item in div:
        sub = item.find('div','newlist').find_all('a',href=lambda x: x and "/b/" in x)
        try:
            for item in sub:
                url = 'http://www.ccv5.com'+item['href']
                titleSub = item['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                r.encoding = r.apparent_encoding
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                href = 'http://www.ccv5.com'+soup.find('div','playbox').find('a',href=lambda x: x and "/vod/" in x)['href']

                import json
                r = requests.get(href)
                r.encoding = r.apparent_encoding
                c = r.text
                soup = BeautifulSoup(c,"html.parser")

                if soup.find('div','player').find('script'):
                    player = soup.find('div','player').find('script').string.replace('var ff_urls=','').replace('\\','').strip("';")
                    playerJson = json.loads(player)
                    for data in playerJson['Data']:
                        playurls = [j for j in data['playurls']]
                        for p in playurls:
                            title = titleSub+'_'+urllib.parse.unquote(p[0].replace('u',r'\u').encode().decode('unicode-escape'))
                            title_null = titleNull(title)
                            host_url = 'http://www.ccv5.com'+p[2]
                            origin_url = p[1]
                            if origin_url.find('http') != -1:
                                origin_osp = origin_url.split('//')[1]
                                if origin_osp.find('www') != -1:
                                    origin_osp = origin_osp.split('www')[1].lstrip('.').split('.')[0]
                                else:
                                    origin_osp = origin_osp.split('.')[0]
                            else:
                                origin_osp = ''
                                origin_url = ''

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'ccv5',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'china',
                                'cnt_writer': '',
                                'origin_url': origin_url,
                                'origin_osp': origin_osp
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("ccv5 크롤링 시작")
    startCrawling()
    print("ccv5 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
