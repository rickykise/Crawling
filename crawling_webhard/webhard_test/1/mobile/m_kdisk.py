import requests,re
import pymysql,time,datetime
import urllib.parse
import json
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

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

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'http://m.kdisk.co.kr/api/content/list.php?cate='+site+'&search_type=title&is_rights=y&adult_not=y&page='
            post_one  = s.post(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)
            try:
                for item in text:
                    if a == 76:
                        break
                    cnt_num = text.split('"idx":')[a].split(',"')[0]
                    a = a+1
                    url = "http://m.kdisk.co.kr/?cate="+site+'&idx='+cnt_num
                    url2 = 'http://m.kdisk.co.kr/api/content/view.php?idx='+cnt_num

                    post_two  = s.post(url2, headers=headers)
                    c = post_two.content
                    soup2 = bs(c.decode('euc-kr','replace'), 'html.parser')
                    text2 = str(json.loads(str(soup2)))
                    cnt_chk = 0

                    title = text2.split("title': '")[1].split("', '")[0].strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    cnt_price = text2.split("point': '")[1].split("', '")[0].replace(",","").strip()
                    cnt_writer = text2.split("up_nickname': '")[1].split("', '")[0].strip()
                    cnt_vol = text2.split("total_file_size': '")[1].split("', '")[0].strip()
                    if text2.find("file_name': '") != -1:
                        cnt_fname = text2.split("file_name': '")[1].split("', '")[0].strip()
                    else:
                        cnt_fnamech = text2.split("file_name': ")[1].split('",')[0].strip()
                        cnt_fname = cnt_fnamech.split('"')[1]
                    jehu = text2.split("is_rights': '")[1].split("', '")[0].strip()
                    if jehu == 'Y':
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'kdisk',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : cnt_fname,
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("kdisk 크롤링 시작")
    site = ['ALL','MOV','DRA','MED','ANI']
    for s in site:
        startCrawling(s)
    print("kdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
