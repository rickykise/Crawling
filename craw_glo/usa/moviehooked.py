import requests
import time
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = "https://moviehooked.com/country/korea/page/{}/"
    while check:
        i = i+1
        if i == 13:
            break
        # print(link.format(str(i)))
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        try:
            div = soup.find('div', id='gmr-main-load')
            article = div.find_all('article')
            for item in article:
                url = item.find('div','content-thumbnail').find('a')['href']
                titleSub = item.find('div','content-thumbnail').find('a')['title'].strip()
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
                sub = soup.find('main', id='main').find('div', 'gmr-listseries').find_all('a','button')
                for item in sub:
                    r1 = requests.get(item['href'])
                    c = r1.content
                    soup = BeautifulSoup(c,"html.parser")
                    server = soup.find('ul','muvipro-player-tabs').find_all('a')
                    for s in server:
                        title = item['title'].strip()+'_'+s.text
                        title_null = titleNull(title)
                        host_url = s['href']
                        if host_url.find('https:') == -1:
                            host_url = 'https://moviehooked.com'+host_url
                        
                        r2 = requests.get(host_url)
                        c = r2.content
                        soup = BeautifulSoup(c,"html.parser")
                        if soup.find('iframe'):
                            origin_url = soup.find('iframe')['src']
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[1]
                        else:
                            origin_url = ''
                            origin_osp = ''

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'moviehooked',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'unitedstates',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")

                        dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("moviehooked 크롤링 시작")
    startCrawling()
    print("moviehooked 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
