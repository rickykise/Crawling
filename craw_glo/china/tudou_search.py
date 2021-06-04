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
    'Cookie': 'SOKUSESSID=1569489162251HWs; isg=BB0dKOQeHDBKDfgczoEx0f3TJPkXOlGM7Hccr9_iWHSjlj3Ip4tMXKeFxFA1TWlE; cna=Cm8TFmBY9zMCAT1SccQHvRD6; __ayspstp=1; __aysid=1569489170419FNA',
    'Host': 'www.soku.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://www.soku.com/nt/search/q_'+keyword+'_orderby_1_limitdate_0?spm=a2h0k.8191414.0.0&site=14&page='
    try:
        while check:
            with requests.Session() as s:
                i = i+1
                if i == 10:
                    break
                post_one  = s.get(link+str(i), headers=headers)
                soup = bs(post_one.text, 'html.parser')
                div = soup.find('div', 'sk-vlist').find_all('div', 'v')

                for item in div:
                    url = 'https://video.tudou.com/v/'+item.find('a')['href'].split('/v/')[1]
                    title = item.find('a')['title']
                    title_null = titleNull(title)

                    # 제외 키워드 체크
                    getEx = ex_del()
                    exRe =  checkEx(title_null, getEx)
                    if exRe['m'] != None:
                        continue

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'tudou',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                        'origin_url': '',
                        'origin_osp': '',
                        'cnt_keyword_nat': k_nat
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
    except:
        pass

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()
    getKey = getKeywordCH()

    print("tudou 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("tudou 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
