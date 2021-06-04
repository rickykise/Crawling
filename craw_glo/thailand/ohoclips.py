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
    i = 0;check = True
    link = "http://www.ohoclips.com/category/{}/page/{}/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(site,str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        h2 = soup.find('div', id='main-content').find_all('h2',"entry-title")

        try:
            for item in h2:
                url = item.find('a')['href']
                titleSub = item.find('a').text
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
                iframe = soup.find('div',id='main-content').find_all('iframe')
                h4 = soup.find('div',id='main-content').find_all('h4')

                for item,item2 in zip(iframe,h4):
                    host_url = item['src']
                    origin_url = host_url

                    if host_url.find('http') == -1:
                        host_url = 'https:'+host_url

                    if origin_url.find('http') == -1:
                        origin_url = 'https:'+origin_url
                    origin_osp = origin_url.split('//')[1]
                    if origin_osp.find('www') != -1:
                        origin_osp = origin_osp.split('www.')[1].split('.')[0]
                    elif origin_osp.find('myqcloud') != -1:
                        origin_osp = 'myqcloud'
                    else:
                        origin_osp = origin_osp.split('.')[0]


                    title = item2.text.strip()
                    if title.find('Ep.') == -1:
                        continue

                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'ohoclips',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': '',
                        'origin_url': origin_url,
                        'origin_osp': origin_osp
                    }
                    print(data)
                    print("=============================")

                    dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("ohoclips 크롤링 시작")
    page = ['korean-series','hit-series-2019']
    for site in page:
        startCrawling(site)
        
    print("ohoclips 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
