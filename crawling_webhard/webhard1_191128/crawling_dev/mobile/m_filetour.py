import requests,re
import pymysql,time,datetime
import urllib.parse
from requests import Session
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from webhardFun import *
from selenium import webdriver
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

def startCrawling(site):
    i = 0;check = True;pn_sd = ''
    with requests.Session() as s:
        while check:
            i = i+1
            if i == 4:
                break
            link = "http://m.filetour.com/mobile/contents?lcate_cd="+site+"&list_cnt=50"
            if pn_sd != '':
                link = 'http://m.filetour.com'+pn_sd+"&list_cnt=50"
            post_one  = s.get(link)
            content = post_one.content
            soup = bs(content.decode('utf-8','replace'), 'html.parser')
            pn_sd = soup.find('div', 'paging').find_all('li')[i].find('a')['href']
            div = soup.find_all('div', 'contents_area')
            try:
                for item in div:
                    text = str(item)
                    if text.find('19금 이미지') != -1:
                        continue
                    cnt_num = item.find('a')['href'].split('contents/')[1]
                    url = 'http://m.filetour.com'+item.find('a')['href']
                    url2 = 'http://www.filetour.com/front/contents/'+cnt_num

                    r = requests.get(url2)
                    c = r.content
                    soup = BeautifulSoup(c,"html.parser")
                    table = soup.find('table', 'show_table')
                    cnt_chk = 0

                    title = soup.find('title').text.strip().split('파일투어 - ')[1]
                    title_null = titleNull(title)
                    # 키워드 체크
                    getKey = getKeyword()
                    keyCheck = checkTitle(title_null, getKey)
                    if keyCheck['m'] == None:
                        continue
                    keyCheck2 = checkTitle2(title_null, getKey)
                    if keyCheck2['m'] == None:
                        continue
                    # checkPrice = str(keyCheck['p'])
                    cnt_price = soup.find('span', 'red-txt bold-txt').text.replace(" ","").replace(",","").strip().split('P')[0]
                    cnt_writer = table.find_all('td')[1].text.strip()
                    cnt_vol = table.find_all('td')[2].text.strip()
                    cnt_fname = table.find_all('tr')[2].find('td').text.strip()
                    if table.find('span', 'b_blue_btn disp_ibl'):
                        jehu = table.find('span', 'b_blue_btn disp_ibl').text.strip()
                        if jehu == '제휴':
                            cnt_chk = 1
                    # if checkPrice == cnt_price:
                    #     cnt_chk = 1

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

    print("m_filetour 크롤링 시작")
    site = ['','MOV','TV','ANI']
    for s in site:
        startCrawling(s)
    print("m_filetour 크롤링 끝")
    print("--- %s seconds ---" %(time.time() - start_time))
    print("=================================")
