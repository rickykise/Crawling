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
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'ACEUCI=1; click_num=1; num_de_cate=1; _offset_=50; __utmz=206882831.1553146391.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); m_gift_url=up0001; __utma=206882831.1911130585.1553146391.1553146391.1553146391.1; cookie_site=megafile.co.kr; event100=Y; __utmc=206882831; rewardtdiskCookie=Y; rewardtdiskCookie_small=Y; rewardjjangfileCookie=Y; rewardjjangfileCookie_small=Y; extra=1; top100=n; a630ba93bd3d9d55b78a4ec6e1e6c06c=5%2BtcVNJSHIEpHM0ZRnN57LkdR4SoubEGZc5ioQmntJM%3D; c16c5fcb93d4d18e9f6943a4e2cd5a7d=acuiS0jr; 28c0baaa868091a3bd386ae021a73bf4=JE0ZbGG%2BeQ%3D%3D; national=1; login_email=up0001%40naver.com; login_session=1501_ad4e2de4d1adcc32a2b9807de60461cd; login_id=8719774; login_loginid=up0001; login_check=56d4d2c3afc9758b57bee4a7d64ac8d8; login_name=up0001; login_nickname=up0001; login_level=2; check_adultk=0; first=1; part_array=%7C%7C%7C0%7C1%7C0; rdate=2019-01-21; rdate2=2019-01-21+14%3A11%3A20; regdate=2019-01-21+14%3A11%3A20; ses_code=7cc4179b53aa2d5a3f49e5b0554854ab; _pk_id.3.4cb7=8237446fdfb65f5f.1553146391.2.1553154059.1553154039.; _pk_ses.3.4cb7=*; ACENASP_CK=http%3A//www.megafile.co.kr/user/login_process.php; m_sess=40%3AB0%3A76%3A9D%3AE8%3A30; ACEFCID=UID-5C9322171F11C388F729CD69',
    'Host': 'www.megafile.co.kr',
    'Referer': 'http://www.megafile.co.kr/webhard/list.php',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest'
}

def startCrawling(site):
    i = 0; a = 1;check = True
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 2:
                break
            Page = {
                'category': site,
                'page': str(i),
                'pagesize': '50',
                'ver': '1553147208174'
            }
            link = 'http://www.megafile.co.kr/webhard/list.php?category='+site+'&page='+str(i)+'&ver=1553147731998&pagesize=50'
            post_one  = s.get(link, headers=headers, data=Page)
            c = post_one.content
            soup = bs(c.decode('euc-kr','replace'), 'html.parser')
            ul = soup.find_all('ul', id='list')
            
            for item in ul:
                text = str(item)
                if text.find('타사이트') != -1 or text.find('성인인증이 필요') != -1:
                    continue
                cnt_num = item.find('input')['value']
                title = item.find('a')['title']
                title_null = titleNull(title)
                id = item.find('a')['onclick'].split('Window2_new(')[1].split(' ,')[0]
                url = 'http://www.megafile.co.kr/webhard/view.php?WriteNum='+cnt_num+'&fv='
                print(url)

                Data = {
                    'fv': '',
                    'WriteNum': cnt_num
                }

                Page = {
                    'id': id,
                    'requested': ''
                }

                post_two  = s.post(url, headers=headers, data=Data)
                post_rq  = s.post(url, headers=headers, data=Page)
                c = post_two2.content
                soup = bs(c.decode('euc-kr','replace'), 'html.parser')
                print(soup)

                print('=========================')
                break
                # break

                # data = {
                #     'Cnt_num' : cnt_num,
                #     'Cnt_osp' : 'megafile',
                #     'Cnt_title': title,
                #     'Cnt_title_null': title_null,
                #     'Cnt_url': url,
                #     'Cnt_price': cnt_price,
                #     'Cnt_writer' : cnt_writer,
                #     'Cnt_vol' : cnt_vol,
                #     'Cnt_fname' : cnt_fname,
                #     'Cnt_chk': cnt_chk
                # }
                # print(data)



if __name__=='__main__':
    start_time = time.time()

    print("megafile 크롤링 시작")
    # site = ['1','2','3','5']
    site = ['1']
    for s in site:
        startCrawling(s)
    print("megafile 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
