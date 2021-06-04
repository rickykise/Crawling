import requests,re
import pymysql,time,datetime
import urllib.parse
import sys,os
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Connection': 'Keep-Alive',
    'Cookie': 'AdskeeperStorage=%7B%220%22%3A%7B%22svspr%22%3A%22%22%2C%22svsds%22%3A2%2C%22TejndEEDj%22%3A%22LuIkJLra1%22%7D%2C%22C344790%22%3A%7B%22page%22%3A1%7D%7D; _popfired=3; _popfired_expires=Invalid%20Date; _popprepop=1; lastOpenAt_=1604037385996; _gid=GA1.2.737548561.1604037329; _ga=GA1.2.1206628307.1604037329; token_QpUJAAAAAAAAGu98Hdz1l_lcSZ2rY60Ajjk9U1c=BAYAX5uq1QFfm6r5gAGBAsAAIPlAbeAZ3JwhD2vQsOudHDSstwz-Lpo4VATXewVZY-3bwQBGMEQCIB6BsP4NCAzqwwuZ_94xGNiwTDpmn691IGoM4NDHRlcPAiBt0zL4A9aYN2sHudv4J76HwEGXaIFN-bXLi_xrFGLnEg; 6US=1; a=DGRTXsRdahV6F4o5N9eEg2V6R8gmSd2t',
    'Host': 'xemphimhay247.com',
    'Referer': 'http://xemphimhay247.com/danh-sach-phim/QuocGia=h%C3%A0n-qu%E1%BB%91c',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'X-Requested-With': 'XMLHttpRequest'
}

def startCrawling():
    i = 0;check = True
    link = "http://xemphimhay247.com/Home/_DanhSachPhimPartialView?page="
    link2 = "&X-Requested-With=XMLHttpRequest&_=1604037367096"
    while check:
        i = i+1
        if i == 30:
            break

        data = {
            '_': '1604037367096',
            'page': str(i),
            'X-Requested-With': 'XMLHttpRequest'
        }
        r = requests.get(link+str(i)+link2, headers=headers, data=data)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(print(link+str(i)+link2))
        div = soup.find_all('div', 'Phim-Cell')

        # try:
        for item in div:
            url = item.find('a')['href']
            titleSub = item.find('div', 'Phim-Cell-TieuDe').text.strip()
            if titleSub.find('(') != -1:
                titleSub = titleSub.split('(')[0].strip()
            title_check = titleNull(titleSub)
            print(url)
            print(titleSub)
            print("=================================")


        #
        #         # 키워드 체크
        #         getKey = getKeyword()
        #         keyCheck = checkTitle(title_check, getKey)
        #         if keyCheck['m'] == None:
        #             continue
        #         cnt_id = keyCheck['i']
        #         cnt_keyword = keyCheck['k']
        #
        #         r = requests.get(url)
        #         c = r.content
        #         soup = BeautifulSoup(c,"html.parser")
        #         url2 = soup.find('a', 'btn-danger')['href']
        #
        #         r = requests.get(url2)
        #         c = r.content
        #         soup = BeautifulSoup(c,"html.parser")
        #         li = soup.find('ul', 'list-episode').find_all('li')
        #
        #         for item in li:
        #             host_url = item.find('a')['href']
        #             titleNum = item.find('a').text.strip()
        #             title = titleSub+'_'+titleNum
        #             title_null = titleNull(title)
        #
        #             data = {
        #                 'cnt_id': cnt_id,
        #                 'cnt_osp' : 'xemphimhay247',
        #                 'cnt_title': title,
        #                 'cnt_title_null': title_null,
        #                 'host_url' : host_url,
        #                 'host_cnt': '1',
        #                 'site_url': url,
        #                 'cnt_cp_id': 'sbscp',
        #                 'cnt_keyword': cnt_keyword,
        #                 'cnt_nat': 'vietnam',
        #                 'cnt_writer': ''
        #             }
        #             print(data)
        #             print("=================================")
        #
        #             # dbResult = insertALL(data)
        # except:
        #     continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xemphimhay247 크롤링 시작")
    startCrawling()
    print("xemphimhay247 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
