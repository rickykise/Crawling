import requests
import time
import json
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR',
    'Cookie': '__cfduid=d3dd31bda66891fa1c3ef80fc4083b7031620113384; cf_chl_prog=; cf_clearance=999f20fbef0bee96399f9179336ee41412a06b52-1620113384-0-150; cf_chl_prog=a11; PHPSESSID=6o28q95tj3qebl9madvqj5vmh1; __tins__20563337=%7B%22sid%22%3A%201620113394741%2C%20%22vd%22%3A%201%2C%20%22expires%22%3A%201620115194741%7D; __51cke__=; __51laig__=1',
    'Host': 'www.dadikan.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
}

def startCrawling(type):
    i = 0;check = True
    link = 'http://www.dadikan.com/video/type{}/-韩国----hits-{}.html'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(type,str(i)), headers=headers)
        print(link.format(type,str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        print(soup)
        li = soup.find('div','channel').find_all('li')

        try:
            for item in li:
                url = 'http://www.dadikan.com'+item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
                print(titleSub)
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
                div = soup.find_all('div', id='stab_11')

                for item in div:
                    li = item.find_all('li')
                    for item in li:
                        host_url = 'http://www.dadikan.com'+item.find('a')['href']
                        title = titleSub+'_'+item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'dadi.tv',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'china',
                            'cnt_writer': ''
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("dadi.tv 크롤링 시작")
    page = ['4','2']
    for item in page:
        startCrawling(item)
    print("dadi.tv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
