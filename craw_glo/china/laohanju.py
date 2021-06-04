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
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(num):
    i = 0;check = True;end=3
    link = 'http://laohanju.com/index.php/ajax/data.html?mid=1&page={}&limit=10&tid={}'
    while check:
        i = i+1
        if i == end:
            break
        if i == 1:
            r = requests.get('http://laohanju.com/vodtype/'+str(num)+'/')
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find_all('a', 'weui-media-box__bd')
            craw = [ {'vod_name':item.find('h4','weui-media-box__title').text.strip(),'vod_id':item['href'].split('/')[2].replace('-1-1','')} for item in soup.find_all('a', 'weui-media-box__bd') ]
            vodURL = 'http://laohanju.com/vodplay/{}-1-1/'
        else:
            r = requests.get(link.format(str(i),str(num)))
            c = r.json()
            end = c['pagecount'] if c['pagecount'] <= 30 else 30
            craw = c['list']
            vodURL = 'http://laohanju.com/vod/{}-1-1.html'
        end = 3
        try:
            for item in craw:
                url = vodURL.format(item['vod_id'])
                titleSub = item['vod_name']
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
                playlist = soup.find_all('ul','myui-playlist')
                if playlist:
                    for p in playlist:
                        vodplay = p.find_all('a')
                        for item in vodplay:
                            host_url = 'http://laohanju.com'+item['href']
                            title = titleSub+'_'+item.text.strip()
                            title_null = titleNull(title)

                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'laohanju',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'china',
                                'cnt_writer': '',
                            }
                            # print(data)
                            # print("=================================")

                            dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("laohanju 크롤링 시작")
    site = [3,2,20]
    for s in site:
        startCrawling(s)
    print("laohanju 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
