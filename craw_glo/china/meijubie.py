import requests
import time
import json
import sys,os
from requests import Session
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from gloFun import *
from bs4 import BeautifulSoup
import inspect
osp_id = inspect.getfile(inspect.currentframe()).split('.')[0]
getDel = ospCheck(osp_id)

def startCrawling(type):
    i = 0;check = True
    link = 'http://www.meijubie.com/search.php?page={}&searchtype=5&order=time&area=&year=&letter=&yuyan=&state=&money=&ver=&jq=&tid={}'
    while check:
        i = i+1
        if i == 30:
            break

        r = requests.get(link.format(str(i),type))
        c = r.text
        soup = BeautifulSoup(c,"html.parser")
        li = soup.find('div','hy-video-list').find_all('li')
        try:
            for item in li:
                url = 'http://www.meijubie.com/' + item.find('a',"videopic lazy")['href']
                titleSub = item.find('a',"videopic lazy")['title'].strip()
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
                sub = soup.find('div','playlist').find_all('a')
                for item in sub:
                    host_url = 'http://www.meijubie.com/'+item['href']
                    title = titleSub+'_'+item['title'].strip()
                    title_null = titleNull(title)

                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'meijubie',
                        'cnt_title': title,
                        'cnt_title_null': title_null,
                        'host_url' : host_url,
                        'host_cnt': '1',
                        'site_url': url,
                        'cnt_cp_id': 'sbscp',
                        'cnt_keyword': cnt_keyword,
                        'cnt_nat': 'china',
                        'cnt_writer': '',
                    }
                    # print(data)
                    # print("=================================")

                    dbResult = insertALL(data)
        except Exception as e:
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("meijubie 크롤링 시작")
    typeArr = ['2','3']
    for t in typeArr:
        startCrawling(t)
    print("meijubie 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
