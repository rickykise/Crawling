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

def startCrawling(param):
    i = 0;check = True
    link = 'https://3978.com/index.php/vod/show/area/%E9%9F%A9%E5%9B%BD/id/{}/lang/%E9%9F%A9%E8%AF%AD/page/{}.html'
    while check:
        i = i+1
        if i == param[1]:
            break
        r = requests.get(link.format(param[0],str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'img-list').find_all('li')

        try:
            for item in li:
                url = 'https://3978.com'+item.find('a')['href']
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
                div = soup.find_all('div', 'video_list')

                for item in div:
                    sub = item.find_all('a')
                    for item in sub:
                        host_url = 'https://3978.com'+item['href']
                        title = titleSub + '_' + item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : '3978.com',
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

    print("3978.com 크롤링 시작")
    page = [['2',30],['3',25]]
    for item in page:
        startCrawling(item)
    print("3978.com 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
