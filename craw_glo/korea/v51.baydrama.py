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

def startCrawling(site):
    i = 1;check = True;cnt_osp = 'v51.baydrama';osp_link = 'https://v52.baydrama.live/'
    getGroup = groupCheck(cnt_osp)
    group_id = getGroup['id']
    group_url = getGroup['url']
    tab = ['1', '2', '3']
    for t in tab:
        if group_id != None:
            osp_link = group_url
            link = group_url+'tv/board/'+site+'/tab_no/'+t+'/page/'
            cnt_osp = group_id
        else:
            link = osp_link+'tv/board/'+site+'/tab_no/'+t+'/page/'

        while check:
            if i == 450:
                break
            r = requests.get(link+str(i))
            if i == 1:
                i = i + 14
            else:
                i = i + 15
            c = r.content
            soup = BeautifulSoup(c,"html.parser")
            sub = soup.find_all('a', 'list-group-item')
            if len(sub) < 1:
                break

            try:
                for item in sub:
                    url = osp_link[:-1]+item['href']
                    del_title = item.find('span').text.strip()
                    titleSub = item.text.split(del_title)[0].strip()
                    title_check = titleNull(titleSub)

                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_check, getKey)
                    if keyCheck['m'] == None:
                        continue
                    cnt_id = keyCheck['i']
                    cnt_keyword = keyCheck['k']

                    r = requests.get(osp_link+url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    sub2 = soup.find_all('center')[1].find_all('a')
                    if soup.find('a', 'btn btn-default btn-block'):
                        cnt_idx = soup.find('a', 'btn btn-default btn-block')['href'].split('brd_detail/')[1].split('/')[0]
                        url2 = osp_link[:-1]+soup.find('a', 'btn btn-default btn-block')['href'].split(cnt_idx+'/')[0]+cnt_idx+'/page/'
                        a = 1; checkSub = True
                        while checkSub:
                            if a == 150:
                                break
                            r = requests.get(url2+str(a))
                            if a == 1:
                                a = a + 14
                            else:
                                a = a + 15
                            c = r.content
                            soup = BeautifulSoup(c,"html.parser")
                            div = soup.find('div', 'list-group').find_all('a')
                            if len(div) < 1:
                                checkSub = False;break

                            for item in div:
                                url3 = osp_link[:-1]+item['href']
                                del_title = item.find('span').text.strip()
                                titleSub = item.text.split(del_title)[0].strip()
                                title_check = titleNull(titleSub)

                                r = requests.get(url3)
                                c = r.content
                                soup = BeautifulSoup(c,"html.parser")
                                sub2 = soup.find_all('center')[1].find_all('a')

                                for item in sub2:
                                    host_url = item['href']
                                    host_url = urllib.parse.unquote(host_url)
                                    title_num = item.text.strip()
                                    title = titleSub+'_'+title_num
                                    title_null = titleNull(title)

                                    data = {
                                        'cnt_id': cnt_id,
                                        'cnt_osp' : cnt_osp,
                                        'cnt_title': title,
                                        'cnt_title_null': title_null,
                                        'host_url' : host_url,
                                        'host_cnt': '1',
                                        'site_url': url,
                                        'cnt_cp_id': 'sbscp',
                                        'cnt_keyword': cnt_keyword,
                                        'cnt_nat': 'southkorea',
                                        'cnt_writer': ''
                                    }
                                    # print(data)
                                    # print("=================================")

                                    dbResult = insertALL(data)
            except:
                continue

if __name__=='__main__':
    start_time = time.time()

    print("v51.baydrama 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("v51.baydrama 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
