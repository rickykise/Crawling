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
        if i == 4:
            break
        r = requests.get('https://pandavod.tv/drama/kr/?page={}'.format(str(i)))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'program__item')

        try:
            for item in div:
                url = 'https://pandavod.tv'+item.find('a')['href']
                titleSub = item.find('div','program__title').text.strip()
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
                links = soup.find_all('a','playlist__link',href=lambda x: x and "/drama/kr/" in x)

                for item in links:
                    host_url = 'https://pandavod.tv'+item['href']
                    title = titleSub + '_' + item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'pandavod',
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

    print("pandavod 크롤링 시작")
    startCrawling()
    print("pandavod 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
