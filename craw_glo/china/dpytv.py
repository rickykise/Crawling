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
    link = "http://www.dpytv.net/pindao/"+param[0]+"/area/%E9%9F%A9%E5%9B%BD/page/{}/"
    while check:
        i = i+1
        if i == param[1]:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('ul', 'stui-vodlist').find_all('li')
        try:
            for item in li:
                url = 'http://www.dpytv.net'+item.find('a')['href']
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
                ul = soup.find_all('ul','stui-content__playlist clearfix')
                for u in ul:
                    sub = u.find_all('a')
                    for item in sub:
                        host_url = 'http://www.dpytv.net'+item['href']
                        title = titleSub+'_'+item.text.strip()
                        title_null = titleNull(title)

                        data = {
                            'cnt_id': cnt_id,
                            'cnt_osp' : 'dpytv',
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

    print("dpytv 크롤링 시작")
    page = [['dianshiju',22],['zongyi',8]]
    for item in page:
        startCrawling(item)
    print("dpytv 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
