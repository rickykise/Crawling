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
    link = 'https://korezi.com/kore-dizileri/page/{}'
    while check:
        i = i+1
        if i == 21:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div', 'list-custom-series').find_all('li')

        try:
            for item in li:
                url = item.find('a')['href']
                titleSub = item.find('a')['title'].strip()
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
                sub = soup.find('div', 'sidebar-season-list')
                if sub:
                    sub = sub.find_all('a')
                    for item in sub:
                        host_url = item['href']
                        title = item.text.strip()
                        title_null = titleNull(title)
                        
                        r = requests.get(host_url)
                        c = r.content
                        soup = BeautifulSoup(c,"html.parser")
                        if soup.find('iframe'):
                            origin_url = soup.find('iframe')['src']
                            origin_osp = origin_url.split('//')[1]
                            if origin_osp.find('www') != -1:
                                origin_osp = origin_osp.split('www.')[1].split('.')[0]
                            else:
                                origin_osp = origin_osp.split('.')[0]
                        else:
                            origin_url = ''
                            origin_osp = ''

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'korezi',
                            'cnt_title': title,
                            'cnt_title_null': title_null,
                            'host_url' : host_url,
                            'host_cnt': '1',
                            'site_url': url,
                            'cnt_cp_id': 'sbscp',
                            'cnt_keyword': cnt_keyword,
                            'cnt_nat': 'turkey',
                            'cnt_writer': '',
                            'origin_url': origin_url,
                            'origin_osp': origin_osp
                        }
                        # print(data)
                        # print("=================================")
                        dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("korezi 크롤링 시작")
    startCrawling()
    print("korezi 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
