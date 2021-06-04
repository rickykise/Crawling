import requests
import time
import sys, os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling():
    i = 0;check = True
    link = "https://xn--12ct0a9ceo5b3cxabf2byg4etc.com/page/{}/"
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        titles = soup.find('div',  id='movie_post_widget-2').find_all('div', "entry-title")

        try:
            for item in titles:
                url = item.find('a')['href']
                titleSub = item.find('a').text
                title_check = titleNull(titleSub)
                
                # 키워드 체크
                getKey = getKeyword()
                keyCheck = checkTitle(title_check,  getKey)
                if keyCheck['m'] == None:
                    continue
                cnt_id = keyCheck['i']
                cnt_keyword = keyCheck['k']

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c, "html.parser")
                playlist = soup.find('article',  id=re.compile('post-+')).find('div', "entry-content").find_all('a',style=lambda value: value and 'color: #3366ff;' in value)


                for item in playlist:
                    host_url = item['href']
                    title = item.text.strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp': 'xn--12ct',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url': host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'thailand',
                        'cnt_writer': ''
                    }
                    # print(data)
                    # print("=============================")

                    dbResult = insertALL(data)
        except:
            continue


if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("xn--12ct 크롤링 시작")
    startCrawling()
    print("xn--12ct 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
