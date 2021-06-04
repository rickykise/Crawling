import requests,re
import pymysql,time,datetime
import urllib.parse
import json
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from checkFun import *

cnt_osp = 'kdisk'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Origin': 'http://m.kdisk.co.kr',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer': 'http://m.kdisk.co.kr/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'PCID=15475363414190116198676; _ga=GA1.3.2038327300.1547536342; blind_advisory=1; keep_query_string=%2Findex.php; _co_t=1548906834; _gid=GA1.3.91246515.1548906850; app_version=0; pageCookie-sub_cate=; pageCookie-search=; pageCookie-sort=; js_evtBnnrNewYear_20190131=true; layerListGuide=true; adult_not=y; pageCookie-adult_not=y; is_rights=y; pageCookie-is_rights=y; id_save=up0001; auto_login=D8GwPTvB2r%2BxyX70F3aYIGSdrKoUaVZyj1QHWaAFaww%3D; mid=0a191a191a191a19h619c619; nick=up0001; cmn_cash=0; bns_cash=0; coupon=0; login_last=1548914611; Lidx=%241%24juuefmpQ%24scUv8XmFxAyQOuZxwUvdq0; charge=no; pageCookie-page_type=; Intro_domain_chk=m.kdisk.co.kr; gnbRolling-posX=0; pageCookie-page=; pageCookie-search_type=; RefUrl=%2F%3Fcate%3DALL%26is_rights%3Dy%26adult_not%3Dy%26idx%3D11825110; pageCookie-cate=ALL; pageCookie-idx=11825110'
}

def main(url, checkNum):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    checkDate = getCntDate(url,checkNum).strftime('%Y-%m-%d %H:%M:%S')
    if now >= checkDate:
        try:
            with requests.Session() as s:
                cnt_num = url.split('idx=')[1]
                url2 = 'http://m.kdisk.co.kr/api/content/view.php?idx='+cnt_num
                post_two  = s.post(url2, headers=headers)
                c = post_two.content
                soup2 = bs(c.decode('euc-kr','replace'), 'html.parser')
                text = str(json.loads(str(soup2)))
                cnt_chk = 0

                jehu = text.split("is_rights': '")[1].split("', '")[0].strip()
                if jehu == 'Y':
                    cnt_chk = 1
        except:
            cnt_chk = 2
        dbUpdate(checkNum,cnt_chk,url)

if __name__=='__main__':
    start_time = time.time()

    getUrl = getSearchUrl(cnt_osp)
    print("m_kdisk check 크롤링 시작")
    for u, c in getUrl.items():
        c = '3' if c[0] == '0' else '2'
        main(u, c)
    print("m_kdisk check 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
