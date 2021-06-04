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
    link = 'https://phimvn2.net/danh-muc/p/10/{}.aspx'
    while check:
        i = i+1
        if i == 30:
            break
        r = requests.get(link.format(str(i)))
        print(link.format(str(i)))
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        div = soup.find_all('div', 'Form2')

        try:
            for item in div:
                if item.find('a'):
                    url = item.find('div','Form2Text').find('a')['href']
                    url = 'https://phimvn2.net/xem/'+url.replace('../','')
                    titleSub = item.find('div','Form2Text').find('a').text
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
                    div2 = soup.find_all('div', 'num_film')
                    for item in div2:
                        sub = item.find_all('a')
                        for item in sub:
                            host_url = 'https://phimvn2.net/xem/'+item['href'].replace('../','')
                            title_num = item.text.strip()
                            title = titleSub+'_'+title_num
                            title_null = titleNull(title)
                            data = {
                                'cnt_id': cnt_id,
                                'cnt_osp' : 'phimbo2',
                                'cnt_title': title,
                                'cnt_title_null': title_null,
                                'host_url' : host_url,
                                'host_cnt': '1',
                                'site_url': url,
                                'cnt_cp_id': 'sbscp',
                                'cnt_keyword': cnt_keyword,
                                'cnt_nat': 'vietnam',
                                'cnt_writer': ''
                            }
                            print(data)
                            print("=================================")

                            dbResult = insertALL(data)
        except Exception as e:
            print(e)
            continue

if __name__=='__main__':
    start_time = time.time()
    if getDel == '1': sys.exit()

    print("phimbo2 크롤링 시작")
    startCrawling()
    print("phimbo2 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
