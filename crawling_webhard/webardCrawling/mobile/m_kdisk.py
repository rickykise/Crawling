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

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = 'https://m.kdisk.co.kr/api/content/list.php?cate='+site+'&search_type=title&adult_not=y&is_nostr=y&page='

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'ko-KR',
                'Connection': 'Keep-Alive',
                'Content-Length': '0',
                'Cookie': 'Intro_domain_chk=m.kdisk.co.kr; keep_query_string=%2Findex.php%3Fmode%3Dkdisk%26section%3DDRA; _co_t=1617950461; _gcl_au=1.1.404653548.1617950462; PCID=16179504617043532235065; _ga=GA1.1.832453019.1617950462; _gid=GA1.3.652132047.1617950462; app_version=0; is_paypage=; pageCookie-cate=MOV; pageCookie-sub_cate=; pageCookie-page_type=; pageCookie-search_type=title; pageCookie-search=; pageCookie-sort=; pageCookie-page=2; pageCookie-idx=; gnbRolling-posX=0; _ga_X3J9M4DJ9W=GS1.1.1617951453.1.1.1617951603.38; pageCookie-is_nostr=y; RefUrl=%2F%3Fcate%3DMOV%26search_type%3Dtitle%26adult_not%3Dy%26is_nostr%3Dy%26page%3D3; layerListGuide=true; adult_not=y; pageCookie-adult_not=y; pageCookie-cate_banner=true; _ga=GA1.4.832453019.1617950462; _gid=GA1.4.652132047.1617950462',
                'Host': 'm.kdisk.co.kr',
                'Referer': link+str(i),
                'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0',
                'X-Requested-With': 'XMLHttpRequest'
            }

            post_one  = s.post(link+str(i), headers=headers)
            soup = bs(post_one.text, 'html.parser')
            text = str(soup)

            try:
                for item in text:
                    if a == 76:
                        break
                    cnt_num = text.split('"idx":"')[a].split('",')[0]
                    a = a+1

                    url = "https://m.kdisk.co.kr/?cate="+site+'&idx='+cnt_num
                    url2 = 'https://m.kdisk.co.kr/api/content/view.php?idx='+cnt_num

                    post_two  = s.post(url2, headers=headers).json()
                    text2 = str(post_two)

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
                    # print("=================================")

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("kdisk 크롤링 시작")
    site = ['DRA','MOV','MED','ANI']
    for s in site:
        startCrawling(s)
    print("kdisk 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
