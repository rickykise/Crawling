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
    i = 0;check = True;a = 0;checkRe = True;cnt_osp = 'bubujatv'
    if site == '1':
        cate = ['1', '2', '4']
        for c in cate:
            getGroup = groupCheck(osp_id)
            group_id = getGroup['id']
            group_url = getGroup['url']
            if group_id != None:
                link = group_url+'playlist/mod_playlist_sort_js/'+c+'/0?page='
                cnt_osp = group_id
            else:
                link = 'https://www.bubujatv.rest/playlist/mod_playlist_sort_js/'+c+'/0?page='
            while check:
                i = i+1
                if i == 30:
                    break
                r = requests.get(link+str(i))
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'each-video')

                try:
                    for item in div:
                        url = item.find('a')['href']
                        url = urllib.parse.unquote(url)
                        titleSub = item.find('a')['title']
                        title_check = titleNull(titleSub)

                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_check, getKey)
                        if keyCheck['m'] == None:
                            continue
                        cnt_id = keyCheck['i']
                        cnt_keyword = keyCheck['k']

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        if  soup.find('p', 'pages').find('a'):
                            subLink = soup.find('p', 'pages').find('a')['id']
                            if subLink.find('page=') != -1:
                                subLink = soup.find('p', 'pages').find('a')['id'].split('page=')[0].strip()+'page='

                                while checkRe:
                                    a = a+1
                                    if a == 30:
                                        break
                                    r = requests.get(subLink+str(a))
                                    c = r.content
                                    soup = BeautifulSoup(c,"html.parser")
                                    div = soup.find('div', id='load_video').find_all('div', 'each-video')

                                    for item in div:
                                        host_url = item.find('a')['href']
                                        host_url = urllib.parse.unquote(host_url)
                                        title = item.find('a')['title']
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
                            else:
                                r = requests.get(subLink)
                                c = r.content
                                soup = BeautifulSoup(c,"html.parser")
                                div = soup.find('div', id='load_video').find_all('div', 'each-video')

                                for item in div:
                                    host_url = item.find('a')['href']
                                    host_url = urllib.parse.unquote(host_url)
                                    title = item.find('a')['title']
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
                        else:
                            div = soup.find('div', id='load_video').find_all('div', 'each-video')

                            for item in div:
                                host_url = item.find('a')['href']
                                host_url = urllib.parse.unquote(host_url)
                                title = item.find('a')['title']
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
    else:
        cate = ['1', '2', '4']
        for c in cate:
            getGroup = groupCheck(osp_id)
            group_id = getGroup['id']
            group_url = getGroup['url']
            if group_id != None:
                link = group_url+'playlist/mod_playlist_sort_js/'+c+'/0?page='
                cnt_osp = group_id
            else:
                link = 'https://www.bubujatv.rest/playlist/mod_playlist_sort_js/'+c+'/0?page='
            while check:
                i = i+1
                if i == 30:
                    break
                r = requests.get(link+str(i))
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                div = soup.find_all('div', 'each-video')

                try:
                    for item in div:
                        url = item.find('a')['href']
                        url = urllib.parse.unquote(url)
                        titleSub = item.find('a')['title']
                        title_check = titleNull(titleSub)

                        # 키워드 체크
                        getKey = getKeyword()
                        keyCheck = checkTitle(title_check, getKey)
                        if keyCheck['m'] == None:
                            continue
                        cnt_id = keyCheck['i']
                        cnt_keyword = keyCheck['k']

                        r = requests.get(url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        if  soup.find('p', 'pages').find('a'):
                            subLink = soup.find('p', 'pages').find('a')['id']
                            if subLink.find('page=') != -1:
                                subLink = soup.find('p', 'pages').find('a')['id'].split('page=')[0].strip()+'page='

                                while checkRe:
                                    a = a+1
                                    if a == 30:
                                        break
                                    r = requests.get(subLink+str(a))
                                    c = r.content
                                    soup = BeautifulSoup(c,"html.parser")
                                    div = soup.find('div', id='load_video').find_all('div', 'each-video')

                                    for item in div:
                                        host_url = item.find('a')['href']
                                        host_url = urllib.parse.unquote(host_url)
                                        title = item.find('a')['title']
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
                            else:
                                r = requests.get(subLink)
                                c = r.content
                                soup = BeautifulSoup(c,"html.parser")
                                div = soup.find('div', id='load_video').find_all('div', 'each-video')

                                for item in div:
                                    host_url = item.find('a')['href']
                                    host_url = urllib.parse.unquote(host_url)
                                    title = item.find('a')['title']
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
                        else:
                            div = soup.find('div', id='load_video').find_all('div', 'each-video')

                            for item in div:
                                host_url = item.find('a')['href']
                                host_url = urllib.parse.unquote(host_url)
                                title = item.find('a')['title']
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

    print("bubujatv 크롤링 시작")
    site = ['1', '2']
    for s in site:
        startCrawling(s)
    print("bubujatv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
