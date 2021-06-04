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
    while check:
        i = i+1
        if i == 3:
            break
        r = requests.get('https://so.tv.sohu.com/list_p1101_p2_p31015_p4-1_p5_p6_p77_p80_p92_p10{}_p11_p12_p13.html'.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'st-list').find_all('li')

        try:
            for item in li:
                url = 'https:'+item.find('strong').find('a')['href']
                titleSub = item.find('strong').find('a')['title'].strip()
                title_check = titleNull(titleSub)

                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check, getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.text
                soup = BeautifulSoup(c,"html.parser")
                
                if soup.find('ul','series2'):
                    links = soup.find_all('li','sera2')
                    for item in links:
                        host_url = 'https:'+item['href']
                        title = titleSub + '_' + item.text.strip()
                        title_null = titleNull(title)
                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'tv.sohu',
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
                else:
                    host_url = url
                    title = titleSub
                    title_null = titleNull(title)
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'tv.sohu',
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
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("sohu 크롤링 시작")
    startCrawling()
    print("sohu 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
