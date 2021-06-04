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

def startCrawling(site):
    i = 0;end=30;check = True
    link = 'https://www.hanfan.cc/{}/page/{}/'
    while check:
        i = i+1
        if i == end:
            break
        r = requests.get(link.format(site,str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")

        if i == 1:
            try:
                pageLi = soup.find('div','pagination').find_all('li')
                end = int(pageLi[len(pageLi)-1].text.replace('共','').replace('页','').strip())
            except:
                pass

        article = soup.find_all('article', 'excerpt')

        try:
            for item in article:
                url = item.find('h2').find('a')['href']

                titleSub = item.find('h2').find('a')['title'].strip()
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
                if soup.find('iframe'):
                    origin_url = soup.find('iframe')['src']
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    if origin_osp.find('player') != -1:
                        origin_osp = origin_osp.replace('video.','').split('.')[1]
                        origin_url = 'https:'+origin_url
                    else:
                        origin_osp = origin_osp.split('.')[0]
                else:
                    continue

                data = {
                    'cnt_id': cnt_id,
                    'cnt_osp' : 'hanfan',
                    'cnt_title': titleSub,
                    'cnt_title_null': title_check,
                    'host_url' : url,
                    'host_cnt': '1',
                    'site_url': url,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'china',
                    'cnt_writer': '',
                    'origin_url': origin_url,
                    'origin_osp': origin_osp
                }
                # print(data)
                # print("=================================")

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("hanfan 크롤링 시작")
    page = ['hanju','variety']
    for site in page:
        startCrawling(site)
    print("hanfan 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
