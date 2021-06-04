import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': '5ff5805ada9e40d87db64b642157907c971da52ec4787429e285e8aca764b05a=fwSfP%2FOSNpHsQOMqTFfKrxUj0cKytQlxxmqI2T8vhqXyVy0KQLHgwX99YwFxa8EYfdL1fH3Zm5PXEGVie8qIMNESx%2BmsoOi5IxaM2X2yGzxWOcHBPVpH5cEHqWd4x%2FCJYrojOLZageHGriY%2FZRtmKU%2BDlN7vJ7HLHOjVyIgDfcE%3D; b2aaf1549248438ebf816f420340a5df41b58d2dcba70e3ce48c734cffba54e1=ZwQ%2FrRsIm0NNKGXMmfct8lasPM0LiepqSrH%2B%2BQ6J9ZIm9CDeqKlkySWyTvUusuwUWOLbiBkefaXmJ%2FqiaJ9R8nITRWS9yvjwxpNy4BkAYZj5SKTMLv7RgPe3uVyIoolwpHMFPb%2B%2FixI%2BB%2BnNg9PBWhklZbtfdwJdNLiKOPs4SIp9aFBQ8bCrktpUX3%2BvdXC3; 4d0d97abfff1633e13f5353ade81dee19602a867565a6f48155663fa56c246e4=wZJ5KNHLpbx6dBI%2FRGTB%2BtwS9LLMameormLDUe4pVYVHaJYQfDsmAUskSrn%2FCBpK%2BXbxoLqxwpdIMz%2F36ZY%2Fb9edTcnEDP9dEQ79grNDY6IGqQPs%2BTVg7LFISPM2QkU6ZTEDllY1myDVGvHIitccuYKyR%2BM3wYXeWB9eKEXlzhYOGp36THReVEQeL0IIyBZa; mid=U4ihElm5P0%2BGved5SLnr6jjxwlsj%2F46Ff%2F6q9uE2FrJCYMwYZI0QWOb%2BMCyJ1%2FtV0snFnmB3p7ucOxVWzdlAwFbI83nLfNUyNsXEGM17%2FqWtOlaXq%2BRXO3qZXPKHUACrq8vnud2a2TTX0%2Bz8GLk5y0wb4njSW3Bpz0wXLOYbdQwJ5I43Y9O2G1V0kKM5xnphDJUGYTkrYLCshqz3FWFA4lnGXzMj5iaZV144KmfBvRPobpTn2TKygSA4BDoNBJNcsy6H8tVDPVOvgu%2BWsWQ2YtieRW%2B8LTn6iT23R7Aqu2BTpAoDEFe7hMJaKvaI9RmNbw7UBBTHn2mWOr%2FCHbr1JFc8gC5ozZUl82ZDXOYecoxeneV05jcZm56SYz3BrxbFKygaIF9VxQtIOGbeSppTIF3%2FTAROqAfyqF7KQMEyQ%2FJNNPLEdfCXk9xPukTm9DfOuMaMbBima3AMHNnFaKWjMLQfY5tR8HPWUKdEhOTU8BhSjBdZ0GKVyVp%2BsXSfNNrDVwLWZeCDlOc9yghtaJBSeJ3Yr1mrKSVXTESy9K1tPkr8vNkZP4G8SAQTXT4nre34%2FTE%2BQje6W0%2FWLhfIt9NHJmLdvM8tK%2BwOPgFS1hJjgwiCtgCCUKGsaNRCi6bWIVwz%2FbgWxzusqzn03%2BP%2FV2csaw%3D%3D; Usr=ehdl0126; nick=ehdl0126; memo_cnt=0; adult=1; grade=0; cmn_cash=0; pnt_cash=500; bns_cash=0; coupon=0; CashCnt=1; Day=Y; sKidSafeFlag=N; LogChk=Y; PHPSESSID=0hu2kgqkmn8bfpo0ct22p69rck',
    'Host': 'm.filebogo.com',
    'User-Agent': 'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Nokia; Lumia 520) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Mobile Safari/537.36 Edge/12.0'
}

def startCrawling(key):
    i = 0;check = True
    print(key)
    with requests.Session() as s:
        while check:
            i = i+1
            print(str(i))
            if i == 30:
                break
            link = "https://m.filebogo.com/storage.php?act=list&mSec=all&sSec=all&Search="+key+"&SearchKey=title&Limit=20&Page="+str(i)
            post_one  = s.post(link, headers=headers)
            soup = bs(post_one.text, 'html.parser')
            li = soup.find('ul', 'list_box').find_all('li')
            if len(li) < 2:
                break

            try:
                for item in li:
                    cnt_num = item.find('a')['href'].split("load_view('")[1].split("',")[0].strip()
                    title = item.find('div', 'info').find('span').text.replace('19\xa0', '').strip()
                    title_null = titleNull(title)
                    key_null = titleNull(key)

                    # 키워드 체크
                    if title_null.find(key_null) == -1:
                        continue

                    cnt_writer = item.find('div', 'info').find('span', 'etc').text.split('|')[1].strip()
                    url = 'https://m.filebogo.com/storage.php?act=view&idx='+cnt_num+'&mSec=all&sSec=all'

                    post_one  = s.post(url, headers=headers)
                    soup = bs(post_one.text, 'html.parser')
                    cnt_chk = 0

                    cnt_vol = soup.find('div', 'file_info').find('span').text.split("(")[1].split(")")[0].strip()
                    cnt_fname = soup.find('div', 'seller_con').find('div', 'selc1').text.strip()
                    # cnt_price = soup.find('select', id='select_down_type').find('option').text.split(")")[1].split("캐시")[0].strip()
                    cnt_price = soup.find('div', id='wrap').find('span', 'fr').text.split("캐시")[0].strip()

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'filebogo',
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

                    dbResult = insertALLM(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    conn = pymysql.connect(host='211.193.58.218',user='autogreen',password='uni1004',db='site', port=3307,charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    getKey = getSearchKeyM(conn,curs)
    conn.close()

    print("m_filebogo 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("m_filebogo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
