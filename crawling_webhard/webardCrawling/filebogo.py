import requests,re
import sys
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'PHPSESSID=rj72fa0njcvm8ksjmsei53ua1c; search_history=%5B%5B%227Y6c7Yq47ZWY7Jqw7Iqk%22%2C%2203.17%22%2C%22%22%2C%22title%22%2C%227Y6c7Yq47ZWY7Jqw7Iqk%22%5D%2C%5B%227Yys7Yq4%22%2C%2203.17%22%2C%22%22%2C%22title%22%2C%227Yys7Yq4%22%5D%2C%5B%227Yys7Yq47ZWY7Jqw7Iqk%22%2C%2203.17%22%2C%22%22%2C%22title%22%2C%227Yys7Yq47ZWY7Jqw7Iqk%22%5D%5D; tab_chk=bbs; idx01=1212988; bbs_history=%5B%221212903%22%2C%221212518%22%5D; 5ff5805ada9e40d87db64b642157907c971da52ec4787429e285e8aca764b05a=fwSfP%2FOSNpHsQOMqTFfKrxUj0cKytQlxxmqI2T8vhqXyVy0KQLHgwX99YwFxa8EYfdL1fH3Zm5PXEGVie8qIMNESx%2BmsoOi5IxaM2X2yGzxWOcHBPVpH5cEHqWd4x%2FCJYrojOLZageHGriY%2FZRtmKU%2BDlN7vJ7HLHOjVyIgDfcE%3D; b2aaf1549248438ebf816f420340a5df41b58d2dcba70e3ce48c734cffba54e1=ZwQ%2FrRsIm0NNKGXMmfct8lasPM0LiepqSrH%2B%2BQ6J9ZIm9CDeqKlkySWyTvUusuwUWOLbiBkefaXmJ%2FqiaJ9R8nITRWS9yvjwxpNy4BkAYZj5SKTMLv7RgPe3uVyIoolwpHMFPb%2B%2FixI%2BB%2BnNg9PBWhklZbtfdwJdNLiKOPs4SIp9aFBQ8bCrktpUX3%2BvdXC3; 4d0d97abfff1633e13f5353ade81dee19602a867565a6f48155663fa56c246e4=wZJ5KNHLpbx6dBI%2FRGTB%2BtwS9LLMameormLDUe4pVYVHaJYQfDsmAUskSrn%2FCBpK%2BXbxoLqxwpdIMz%2F36ZY%2Fb9edTcnEDP9dEQ79grNDY6IGqQPs%2BTVg7LFISPM2QkU6ZTEDllY1myDVGvHIitccuYKyR%2BM3wYXeWB9eKEXlzhYOGp36THReVEQeL0IIyBZa; mid=U4ihElm5P0%2BGved5SLnr6jjxwlsj%2F46Ff%2F6q9uE2FrJCYMwYZI0QWOb%2BMCyJ1%2FtV0snFnmB3p7ucOxVWzdlAwFbI83nLfNUyNsXEGM17%2FqWtOlaXq%2BRXO3qZXPKHUACrq8vnud2a2TTX0%2Bz8GLk5y0wb4njSW3Bpz0wXLOYbdQwJ5I43Y9O2G1V0kKM5xnphDJUGYTkrYLCshqz3FWFA4lnGXzMj5iaZV144KmfBvRPobpTn2TKygSA4BDoNBJNcsy6H8tVDPVOvgu%2BWsWQ2YtieRW%2B8LTn6iT23R7Aqu2BTpAoDEFe7hMJaKvaI9RmNbw7UBBTHn2mWOr%2FCHbr1JFc8gC5ozZUl82ZDXOYecoxeneV05jcZm56SYz3BrxbFKygaIF9VxQtIOGbeSppTIF3%2FTAROqAfyqF7KQMEyQ%2FJNNPLEdfCXk9xPukTm9DfOuMaMbBima3AMHNnFaKWjMLQfY5tR8HPWUKdEhOTU8BhSjBdZ0GKVyVp%2BsXSfNNrDVwLWZeCDlOc9yghtaJBSeJ3Yr1mrKSVXTESy9K1tPkr8vNkZP4G8SAQTXT4nre34%2FTE%2BQje6W0%2FWLhfIt9NHJmLdvM8tK%2BwOPgFS1hJjgwiCtgCCUKGsaNRCi6bWIVwz%2FbgWxzusqzn03%2BP%2FV2csaw%3D%3D; Usr=ehdl0126; nick=ehdl0126; memo_cnt=0; adult=1; grade=0; cmn_cash=0; pnt_cash=500; bns_cash=0; coupon=0; CashCnt=1; Day=Y; sKidSafeFlag=N; LogChk=Y',
    'Host': 'www.filebogo.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 10:
                break
            try:
                link = 'https://www.filebogo.com/main/storage.php?search_type='+site+'&p='
                post_one  = s.get(link+str(i), headers=headers)
                soup = bs(post_one.text, 'html.parser')
                ul = soup.find('div', 'list_div').find_all('ul')

                for item in ul:
                    cnt_num = item.find('input')['value'].strip()
                    title = item.find('li', 'sty_li_2').text.replace('19\xa0', '').strip()
                    title_null = titleNull(title)
                    url = 'https://www.filebogo.com/main/popup.php?doc=bbsInfo&idx='+cnt_num
                    cnt_vol = item.find('li', 'sty_li_3').text.strip()
                    cnt_writer = item.find_all('li', 'sty_li_3')[1].text.strip()

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('filebogo',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('filebogo',title,title_null,url)
                        continue

                    post_two  = s.get(url, headers=headers)
                    soup2 = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    cnt_fname = soup2.find('div', id='file_info_detail').find('li').text.strip()
                    cnt_price = soup2.find('div', 'con_info').find_all('div')[1].find_all('li')[5].text.replace(",","").strip()

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

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("filebogo 크롤링 시작")
    site = ['MED','all', 'MOV', 'ANI']
    for s in site:
        startCrawling(s)
    print("filebogo 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
