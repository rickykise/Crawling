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
    'Connection': 'Keep-Alive',
    'Host': 'so.iqiyi.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2]; cnt_osp = 'iqiyi'
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://so.iqiyi.com/so/q_'+keyword+'_ctg__t_0_page_'
    link2 = '_p_1_qc_0_rd__site__m_1_bitrate__af_0'
    try:
        while check:
            with requests.Session() as s:
                i = i+1
                if i == 10:
                    break
                post_one  = s.get(link+str(i)+link2, headers=headers)
                soup = bs(post_one.text, 'html.parser')
                div = soup.find_all('div', 'qy-search-result-item')

                for item in div:
                    if len(item['class']) > 1:
                        continue
                    url = item.find('div', 'result-right').find('a')['href']
                    if url.find('youku') != -1:
                        cnt_osp = 'youku'
                    elif url.find('bilibili') != -1:
                        cnt_osp = 'bilibili'
                    else:
                        cnt_osp = 'iqiyi'

                    if cnt_osp == 'youku':

                    title = item.find('div', 'result-right').find('a')['title']
                    title_null = titleNull(title)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    if url.find('http') == -1:
                        url = 'https:'+url

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : cnt_osp,
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

    print("iqiyi 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("iqiyi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
