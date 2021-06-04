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
    link = 'https://www.j8dy.com/vod/list/2-%E9%9F%A9%E5%9B%BD-------{}---.html'
    while check:
        i = i+1
        if i == 10:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'vodlist').find_all('li','vodlist_item')

        try:
            for item in li:
                url = 'https://www.j8dy.com'+item.find('a')['href']
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
                btn = soup.find('a',{'class':['btn','btn_primary','hplayurl']})
                if btn:
                    r = requests.get('https://www.j8dy.com'+btn['href'])
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    video = soup.find('ul', 'content_playlist').find_all('li')
                    for item in video:
                        host_url = 'https://www.j8dy.com'+item.find('a')['href']
                        title = titleSub+'_'+item.find('a').text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'j8dy',
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
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("j8dy 크롤링 시작")
    startCrawling()
    print("j8dy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
