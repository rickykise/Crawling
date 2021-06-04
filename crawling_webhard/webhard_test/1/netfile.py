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

LOGIN_INFO = {
    'action_event': 'memberLogin',
    'enid': 'dXAwMDAz',
    'id': 'up0003',
    'passwd': 'up0003',
    'pwd': 'dXAwMDAz',
    'url': '/index_front.jsp'
}

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'pop_170926=check; wcs_bt=3bc7e16471d78:1553837240; JSESSIONID=3579B3EE15AFF7AE9C816992ABBA95BC; referer_url=direct; __utmz=210917130.1553745088.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=210917130.662225564.1553745088.1553757728.1553834516.4; __utmb=210917130.47.10.1553834516; __utmc=210917130; __utmt=1',
    'Host': 'www.netfile.co.kr',
    'Referer': 'https://www.netfile.co.kr/index_front.jsp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        login_req = s.post('http://www.netfile.co.kr/member-action.do', headers=headers, data=LOGIN_INFO)
        while check:
            i = i+1
            if i == 2:
                break
            link = 'http://www.netfile.co.kr/index_front.jsp?popok=0&gubunA='+site+'&customer=up0003'
            post_one  = s.get(link)
            soup = bs(post_one.text, 'html.parser')
            tr = soup.find('table', 'bbs').find('tbody').find_all('tr')

            try:
                for item in tr:
                    adult = item.find('a')['href'].split("','")[2].split("'")[0]
                    if adult == '18':
                        continue
                    id = item.find('a')['href'].split("','")[1].split("'")[0]
                    cnt_num = item.find('a')['href'].split("view('")[1].split("','")[0]
                    cate = item.find('a')['href'].split("','")[4].split("'")[0]
                    url = 'http://www.netfile.co.kr/media/view.jsp?fr_id='+cnt_num+'&gid='+id+'&gubun2='+cate
                    title = item.find('a').text.strip()
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        dbResult = insertDB('netfile',title,title_null,url)
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        dbResult = insertDB('netfile',title,title_null,url)
                        continue
                    checkPrice = str(keyCheck['p'])
                    cnt_vol = item.find_all('td', 'data')[0].text.strip()
                    cnt_writer = item.find_all('td', 'data')[1].text.strip()

                    post_two  = s.get(url)
                    soup = bs(post_two.text, 'html.parser')
                    cnt_chk = 0

                    cnt_price = soup.find('span', 'coin').text.split("코인")[0].replace(',', '').strip()
                    if checkPrice == cnt_price:
                        cnt_chk = 1

                    data = {
                        'Cnt_num' : cnt_num,
                        'Cnt_osp' : 'netfile',
                        'Cnt_title': title,
                        'Cnt_title_null': title_null,
                        'Cnt_url': url,
                        'Cnt_price': cnt_price,
                        'Cnt_writer' : cnt_writer,
                        'Cnt_vol' : cnt_vol,
                        'Cnt_fname' : '',
                        'Cnt_chk': cnt_chk
                    }
                    # print(data)

                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("netfile 크롤링 시작")
    site = ['W','M','D','I']
    for s in site:
        startCrawling(s)
    print("netfile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
