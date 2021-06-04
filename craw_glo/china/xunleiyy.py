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
    link = 'https://www.xunleiyy.com/search.php?page={}&searchtype=5&order=time&tid=15&area=&year=&letter=&yuyan=&state=&money=&ver=&jq='
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find('div','list_lis').find_all('div', 'list_lis_mov')

        try:
            for item in div:
                url = 'https://www.xunleiyy.com'+item.find('a')['href']
                titleSub = item.find('img')['alt']
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
                li = soup.find('div','p_list_02').find_all('li')

                for item in li:
                    host_url = 'https://www.xunleiyy.com'+item.find('a')['href']
                    title = titleSub + '_' + item.find('a')['title'].strip()
                    title_null = titleNull(title)

                    r = requests.get(host_url)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    data = {
                        'cnt_id': cnt_id,
                        'cnt_osp' : 'xunleiyy',
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

    print("xunleiyy 크롤링 시작")
    startCrawling()
    print("xunleiyy 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")