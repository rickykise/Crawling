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
path = inspect.getfile(inspect.currentframe())
x = path.split('\\')
x.reverse()
osp_id = x[0].split('.py')[0].strip()

def startCrawling(site):
    i = 0;check = True;cnt_osp = 'l29.hobaktv'; osp_link = 'https://l29.hobaktv.xyz'
    getGroup = groupCheck(osp_id)
    group_id = getGroup['id']
    group_url = getGroup['url']
    if group_id != None:
        osp_link = group_url[:-1]
        link = group_url+site+'/p'
        cnt_osp = group_id
    else:
        link = 'https://l29.hobaktv.xyz/'+site+'/p'
    while check:
        checkSub = True
        i = i+1
        if i == 30:
            break
        r = requests.get(link+str(i))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('td', 'list-subject')

        try:
            for item in div:
                url = osp_link+item.find('a')['href']
                url = urllib.parse.unquote(url)
                title = item.find('a').text.strip()
                title_null = titleNull(title)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_null, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                if soup.find('button', 'baseLinkButton malibu'):
                    url2 = osp_link+soup.find('button', 'baseLinkButton malibu')['onclick'].split("('")[1].split("')")[0]
                    url2 = urllib.parse.unquote(url2)

                    r = requests.get(url2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    td = soup.find_all('td', 'list-subject')

                    for item in td:
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)
                        url3 = osp_link+item.find('a')['href']
                        url3 = urllib.parse.unquote(url3)

                        r = requests.get(url3)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        button = soup.find_all('button', 'baseLinkButton', style="width:50%")

                        for item in button:
                            host_url = item['onclick']
                            if host_url.find("DoLinkToNewWindow('") != -1:
                                host_url = item['onclick'].split("DoLinkToNewWindow('")[1].split("','")[0]

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
                else:
                    td = soup.find_all('td', 'list-subject')
                    for item in td:
                        title = item.find('a').text.strip()
                        title_null = titleNull(title)
                        url2 = osp_link+item.find('a')['href']
                        url2 = urllib.parse.unquote(url2)

                        r = requests.get(url2)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        button = soup.find_all('button', 'baseLinkButton', style="width:50%")

                        for item in button:
                            host_url = item['onclick'].split("DoLinkToNewWindow('")[1].split("','")[0]
                            if host_url.find("DoLinkToNewWindow('") != -1:
                                host_url = item['onclick'].split("DoLinkToNewWindow('")[1].split("','")[0]

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

    print("l29.hobaktv 크롤링 시작")
    site = ['show/enter/section/ing', 'show/enter/section/end', 'show/drama/section/ing', 'show/drama/section/end']
    for s in site:
        startCrawling(s)
    print("l29.hobaktv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
