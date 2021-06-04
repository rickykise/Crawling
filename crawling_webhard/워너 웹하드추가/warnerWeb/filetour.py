import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from bs4 import BeautifulSoup

def startCrawling(key):
    print('키워드: '+key)
    i = 0;check = True;pn_sd = ''
    link = "http://www.filetour.com/front/contents?sword="+key+"&list_cnt=50"
    while check:
        if pn_sd != '':
            link = 'http://www.filetour.com'+pn_sd
        i = i+1
        if i == 30:
            break
        r = requests.get(link)
        c = r.content
        soup = BeautifulSoup(c,"html.parser")
        try:
            div = soup.find('div', 'list_contents')
            ul = div.find_all('ul', 'list_body2')
            pn_sd = soup.find('div', 'paginator_content').find_all('li')[i+2].find('a')['href']

            for item in ul:
                if item.find('span', 'icon-img icon-19'):
                    continue
                cnt_num = item.find('a')['href'].split("contents/")[1]
                url = 'http://www.filetour.com/front/contents/'+cnt_num

                r = requests.get(url)
                c = r.content
                soup = BeautifulSoup(c,"html.parser")
                table = soup.find('table', 'show_table')
                cnt_chk = 0

                title = soup.find('title').text.strip().split('파일투어 - ')[1]
                title_null = titleNull(title)
                key_check = key.replace(' ','')
                if title_null.find(key_check) == -1:
                    continue
                cnt_price = soup.find('span', 'red-txt bold-txt').text.replace(" ","").replace(",","").strip().split('P')[0]
                cnt_writer = table.find_all('td')[1].text.strip()
                cnt_vol = table.find_all('td')[2].text.strip()
                cnt_fname = table.find_all('tr')[2].find('td').text.strip()
                if table.find('span', 'b_blue_btn disp_ibl'):
                    jehu = table.find('span', 'b_blue_btn disp_ibl').text.strip()
                    if jehu == '제휴':
                        cnt_chk = 1

                data = {
                    'Cnt_num' : cnt_num,
                    'Cnt_osp' : 'filetour',
                    'Cnt_title': title,
                    'Cnt_title_null': title_null,
                    'Cnt_url': url,
                    'Cnt_price': cnt_price,
                    'Cnt_writer' : cnt_writer,
                    'Cnt_vol' : cnt_vol,
                    'Cnt_fname' : cnt_fname,
                    'Cnt_chk': cnt_chk
                }
                # print(data)

                dbResult = insertALL(data)
        except:
            continue

if __name__=='__main__':
    start_time = time.time()
    getKey = getWSearchKey()

    print("filetour 크롤링 시작")
    for key in getKey:
        startCrawling(key)
    print("filetour 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
