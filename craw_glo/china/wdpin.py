import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(craw):
    i = 0;check = True
    while check:
        i = i+1
        if i == craw['end']:
            break
        r = requests.get(craw['link'].format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find_all('li','vodlist_item')
        try:
            for item in li:
                url = 'https://wdpin.com'+item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                sub = soup.find('ul', 'content_playlist').find_all('a',href=lambda x: x and "/vodplay/" in x)

                for item in sub:
                    host_url = 'https://wdpin.com'+item['href']
                    
                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    origin_url = str(soup).split('player_data=')[1].split('"url":"')[1].split('",')[0].strip().replace('\\', '')
                    origin_osp = origin_url.split('//')[1]
                    if origin_url.find('http') == -1:
                        origin_url = 'http:'+origin_url
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    elif origin_osp.find('tv.') != -1:
                        origin_osp = origin_osp.split('tv.')[1].split('.')[0]
                    elif origin_osp.find('v.') != -1:
                        origin_osp = origin_osp.split('v.')[1].split('.')[0]
                    else:
                        origin_osp = origin_osp.split('.')[0]
                    
                    title = titleSub+'_'+item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'wdpin',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': 'https://jx.5qx.top/?url=' + origin_url,
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

    print("wdpin 크롤링 시작")
    site = [{'link':'https://wdpin.com/vodshow/15--------{}---.html','end':23},{'link':'https://wdpin.com/vodshow/3-%E6%97%A5%E9%9F%A9-------{}---.html','end':3}]
    for item in site:
        startCrawling(item)
    print("wdpin 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
