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
from requests_toolbelt.multipart.encoder import MultipartEncoder
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(getLink):
    i = 0;check = True
    link = getLink
    while check:
        i = i+1
        if i == 30:
            break
        print(str(i))
        files = {'post_value': (None, i)}
        data = requests.Request('POST', link, files=files).prepare().body.decode('utf8')
        mp_encoder = MultipartEncoder(
            fields={
                'post_value': str(i)
            }
        )

        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Cache-Control': 'no-cache',
            'Connection': 'Keep-Alive',
            'Content-Type': mp_encoder.content_type,
            'Cookie': 'PHPSESSID=cvijnhiei1qduq9tepjoc77885; PC_popup_salaphim_v1_1059am2282020=1; PC_popup_salaphim_auto_608am8132020=1; js_session1=0a248e0e17b2726b-3491382b7295bfbf3b7e512d-c2564b9c5010680c40d42bc27c48ee67f9a4de54427ecbd40bbe8cc90932; PC_popup_salaphim_auto=1; _gat=1; _gid=GA1.2.1521047569.1599020759; _ga=GA1.2.1634822863.1599020759; PC_popup_salaphim_auto_1059am2282020=1; PC_popup_salaphim_v2_1059am2282020=1',
            'Host': 'salaphim.com',
            'Referer': link,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        try:
            r = requests.post(link, data=data, headers=headers)
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            div = soup.find_all('div', id='product_body')

            for item in div:
                url = item.find('a')['href']
                titleSub = item.find('img')['alt']
                print(titleSub)
                if titleSub.find('(') != -1:
                    titleSub = titleSub.split('(')[0].strip()
                title_check = titleNull(titleSub)


                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                print('통과')
                print("=================================")

                headers2 = {
                    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Connection': 'Keep-Alive',
                    'Cookie': 'PHPSESSID=cvijnhiei1qduq9tepjoc77885; PC_popup_salaphim_v1_1059am2282020=1; PC_popup_salaphim_auto_608am8132020=1; js_session1=0a248e0e17b2726b-3491382b7295bfbf3b7e512d-c2564b9c5010680c40d42bc27c48ee67f9a4de54427ecbd40bbe8cc90932; PC_popup_salaphim_auto=1; _gid=GA1.2.1521047569.1599020759; _ga=GA1.2.1634822863.1599020759; PC_popup_salaphim_auto_1059am2282020=1; PC_popup_salaphim_v2_1059am2282020=1',
                    'Host': 'salaphim.com',
                    'Referer': link,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                }

                r = requests.get(url, headers=headers2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                url2 = soup.find('div', id='an_hien_tap_phim_vip').find('a')['href']
                headersUrl = url2.split('-tap')[0].strip()

                headers3 = {
                    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Connection': 'Keep-Alive',
                    'Cookie': 'PHPSESSID=s29nadqm197rimi4t73ispuv16; PC_popup_salaphim_v1_1059am2282020=1; PC_popup_salaphim_auto_608am8132020=1; js_session1=2b71d595c7fcc50a-dda3b616af22a7d971673beb-27b0888d4f097a9d896d001f42cf738b886ffda1bfcac1dd70274704b910; PC_popup_salaphim_auto=1; _gid=GA1.2.488665431.1599024216; QuanVuongBatDietTap11576770746=3; _ga=GA1.2.1691802179.1599024216; PC_popup_salaphim_auto_1059am2282020=1; PC_popup_salaphim_v2_1059am2282020=1; QuanVuongBatDietTap11576770746onerrorvideo=1; _zsfp=_zgna; __zi=2000.SSZzejyD2zydY_whsW5Lr26BykIN71lQESckzfq22PWhtxpvmmaDt6BNiVN21mVSAj6t-OS60D4XrxJzEJ8.1',
                    'Host': 'salaphim.com',
                    'Referer': headersUrl,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                }

                r = requests.get(url2, headers=headers3)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'chon_tap_all')

                for item in div:
                    host_url = item.find('a')['href']
                    title = titleSub+'_'+item.find('a').text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': 'cnt_id',
                        'cnt_osp' : 'salaphim',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': 'cnt_keyword',
                        'cnt_nat': 'vietnam',
                        'cnt_writer': ''
                    }
                    print(data)
                    print("=================================")

                    # dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("salaphim 크롤링 시작")
    url = ['http://salaphim.com/the-loai/phim-han-quoc/','http://salaphim.com/the-loai/phim-tam-ly-tinh-cam/']
    for u in url:
        startCrawling(u)
    print("salaphim 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
