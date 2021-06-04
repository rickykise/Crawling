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
    'Cookie': '_uab_collina=161242505199302785707501; __ayft=1612425052717; __arpvid=16124254613152AXEsv-1612425461331; __ayscnt=1; __aypstp=7; P_ck_ctl=960456E579A86669E5E055208CE39DB4; __arycid=dd-1-00; __arcms=dd-1-00; __ayvstp=6; xlly_s=1; tfstk=cibRBPm2c-2oESNXIgEmdWL27uwGwJyphbO-J5vp6nxRZdCAGRcDPM8jKopG.; __aysvstp=6; isg=BG9vMtrHU_3lb1fB1nAQPaxt-IN5FMM26nFu5YH8717k0I7SieUvhGwSVFpus5uu; redMarkRead=1; __ysuid=1612425052717K0K; _m_h5_tk_enc=16bec662e0b5be871fb076ccd7ac5d48; modalFrequency={"UUID":"2"}; cna=XJWiGNnarQwCAXmMkh+BHzKa; _m_h5_tk=c73f02d62da82ee1ba2bc5934a754dbf_1612430100918; l=eBxr9V5rjPfPvHUEBOfahurza77OSQdYYuPzaNbMiOCP_-5B5NmfW6MGoP86C36Oh6Y9R3RwnC-vBeYBq7Vonxvt1b1P-wDmn; __ayspstp=7; youku_history_word=%5B%22running%2520man%22%5D; __aysid=161242505271742c; ctoken=FsHDyXyc9YlKo-w9CnRYSKby; x5sec=7b22617365727665722d686579693b32223a223437653236366439663463616263646635663931366133346436363632353834434e764f376f4147454a3741686f6a54766275594a54436e325a696a42413d3d227d',
    'Host': 'so.youku.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(key, keyItem):
    keyword = key;cnt_id = keyItem[0];cnt_keyword = keyItem[1];k_nat = keyItem[2];a=1
    print('키워드: '+keyword)
    i = 0;check = True
    link = 'https://so.youku.com/search_video/q_running%20man?spm=a2h0k.11417342.pageturning.dpagenumber&aaid=bd804136a77871f8f98dba528932ef2b&pg='

    try:
        while check:
            with requests.Session() as s:
                i = i+1
                if i == 10:
                    break
                post_one  = s.get(link+str(i), headers=headers)
                soup = bs(post_one.text, 'html.parser')
                text = str(soup)

                for item in text:
                    group_id = text.split('videoId":"')[a].split('","')[0]
                    url = 'https://v.youku.com/v_show/id_'+group_id+'.html'
                    title = text.split('displayName":"')[a].split('","')[0].strip()
                    title_null = titleNull(title)
                    a = a+1
                    if a == 84:
                        a = 1
                        break

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
                        'cnt_osp' : 'youku',
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

    print("youku 크롤링 시작")
    for k, i in getKey.items():
        startCrawling(k, i)
    print("youku 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
