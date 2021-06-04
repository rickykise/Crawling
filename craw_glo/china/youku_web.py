import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from selenium import webdriver
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': '_uab_collina=156948892457272125648616; CNZZDATA1277958921=1240418131-1569485986-https%253A%252F%252Fso.youku.com%252F%7C1570177247; ctoken=ryr8nbuzqj0Xm3WbeJBHmha5; isg=BD8_wr-NXuGVklrmQDCJikzpxhPJJJPGGmE-ddENie414F9i2f3cFrxiJGq7o2s-; __ysuid=1569489162251HWs; UM_distinctid=16d6cd816ba38-07a36b619c1fb28-677b7726-2a3000-16d6cd816bb15e; __artft=1569489170; cna=Cm8TFmBY9zMCAT1SccQHvRD6; __aryft=1569489170; __ayft=1570179126484; __aysid=1570179126485W05; __arpvid=1570179126485OQJT5O-1570179126496; __ayscnt=1; __aypstp=1; __ayspstp=1; P_ck_ctl=8B7E940A7E0957186A730250C6C90C0F',
    'Host': 'so.youku.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://so.youku.com/search_video/q_'+keyword+'?spm=a2h0k.11417342.pageturning.dpagenumber&aaid=bd804136a77871f8f98dba528932ef2b&pg='
    # try:
    while check:
        with requests.Session() as s:
            i = i+1
            if i == 10:
                break
            print(link+str(i))
            post_one  = s.get(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            print(text)

    #             for item in text:
    #                 url = 'https://v.youku.com/v_show/'+text.split('//v.youku.com/v_show/')[a].split('.html')[0]
    #                 a = a+1
    #                 if a == 84:
    #                     a = 1
    #                     break
    #
    #                 post_two = s.get(url)
    #                 soup = bs(post_two.text, 'html.parser')
    #                 title = soup.find('div', 'title-wrap').find('span', 'subtitle').text.strip()
    #                 title_null = titleNull(title)
    #
    #                 # 제외 키워드 체크
    #                 getEx = ex_del()
    #                 exRe =  checkEx(title_null, getEx)
    #                 if exRe['m'] != None:
    #                     continue
    #
    #                 # 키워드 체크
    #                 getKey = getKeyword()
    #                 keyCheck = checkTitle(title_null, getKey)
    #                 if keyCheck['m'] == None:
    #                     continue
    #                 cnt_id = keyCheck['i']
    #                 cnt_keyword = keyCheck['k']
    #
    #                 data = {
    #                     'cnt_id': cnt_id,
    #                     'cnt_osp' : 'youku',
    #                     'cnt_title': title,
    #                     'cnt_title_null': title_null,
    #                     'host_url' : url,
    #                     'host_cnt': '1',
    #                     'site_url': url,
    #                     'cnt_cp_id': 'sbscp',
    #                     'cnt_keyword': cnt_keyword,
    #                     'cnt_nat': 'china',
    #                     'cnt_writer': '',
    #                     'origin_url': '',
    #                     'origin_osp': '',
    #                     'cnt_keyword_nat': k_nat
    #                 }
    #                 print(data)
    #                 print("=================================")
    #
    #                 # dbResult = insertALL(data)
    # except:
    #     pass

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getKey = getKeywordCH()

    print("youku 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("youku 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
