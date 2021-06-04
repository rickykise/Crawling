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

def startCrawling():
    i = 0;check = True
    link = 'http://xemphimhay.net/country/han-quoc/page/'
    while check:
        i = i+1
        if i == 30:
            break

        headers = {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ko-KR',
            'Connection': 'Keep-Alive',
            'Cookie': '__cfduid=d257f70dd577eed4bd447eb0f488a51591618880160; vDDoS=b9ae82f477e5fc8f75619df2d0bc53ec; PHPSESSID=hoqqfa79kd3am3hn1cc7gflvtr; _ga=GA1.2.1545724628.1618880173; _gid=GA1.2.1073410259.1618880173',
            'Host': 'xemphimhay.net',
            'Referer': link+str(i)+'?d=1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }

        r = requests.get(link+str(i)+'?d=1', headers=headers)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        article = soup.find_all('article', 'grid-item')

        try:
            for item in article:
                url = item.find('a')['href']
                titleSub = item.find('a')['title']
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url, headers=headers)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                url2 = soup.find('a', 'btn-danger')['href']
                urlKey = url2.split('xem-phim-')[1].split('/')[0].strip()
                url3 = 'http://zingtvn.net/xem-phim/'+urlKey+'-tap-1-server-1/'

                headers2 = {
                    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'ko-KR',
                    'Connection': 'Keep-Alive',
                    'Cookie': '__cfduid=d4cb3bc646f26385531b1aa5e682ac1d81618881057; _ga=GA1.2.2035678727.1618881058; _gid=GA1.2.572336621.1618881058',
                    'Host': 'zingtvn.net',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
                }
                r = requests.get(url3, headers=headers2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                postid = soup.find('link', rel="shortlink")['href'].split('p=')[1].strip()
                ajax_url = 'http://zingtvn.net/wp-admin/admin-ajax.php'

                data = {
                    'action':'halim_ajax_get_server_list',
                    'episode':'1',
                    'postid': postid,
                    'server':'1'

                }
                r = requests.post(ajax_url,data=data, headers=headers2)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                li = soup.find_all('li', 'halim-episode')

                for item in li:
                    if item.find('a'):
                        host_url = item.find('a')['href']
                        titleNum = item.find('a').text.strip()
                        title = titleSub+'_'+titleNum
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'xemphimhay',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
                    else:
                        host_url = item.find('span')['data-href']
                        titleNum = item.find('span').text.strip()
                        title = titleSub+'_'+titleNum
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'xemphimhay',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'vietnam',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xemphimhay 크롤링 시작")
    startCrawling()
    print("xemphimhay 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
